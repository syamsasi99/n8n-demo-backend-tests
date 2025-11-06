"""
OAuth Token Generator for Google Drive

Run this script ONCE locally to generate OAuth refresh token.
This token will be used in GitHub Actions for automated uploads.

Prerequisites:
1. Enable Google Drive API in Google Cloud Console
2. Create OAuth 2.0 credentials (Desktop app type)
3. Download credentials.json file
4. Place credentials.json in this directory

Usage:
    python get_oauth_token.py

This will:
1. Open your browser for OAuth consent
2. Generate token.json with refresh token
3. Display the token.json contents to copy to GitHub Secrets
"""
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Only request access to files created by this app
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def generate_oauth_token():
    """Generate OAuth refresh token for Google Drive API"""

    creds = None

    # Check if we already have a token
    if os.path.exists('token.json'):
        print("→ Found existing token.json")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if creds and creds.valid:
            print("✓ Existing token is still valid!")
            display_token_info(creds)
            return creds

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("⟳ Refreshing expired token...")
            creds.refresh(Request())
        else:
            # Check for credentials.json
            if not os.path.exists('credentials.json'):
                print("✗ Error: credentials.json not found!")
                print("\nPlease follow these steps:")
                print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
                print("2. Enable Google Drive API")
                print("3. Create OAuth 2.0 credentials (Desktop app type)")
                print("4. Download credentials.json")
                print("5. Place it in this directory")
                print("6. Run this script again")
                return None

            print("→ Starting OAuth flow...")
            print("→ Your browser will open for authentication")

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )

            # CRITICAL: access_type='offline' is required to get refresh token
            # prompt='consent' forces the consent screen to show refresh token
            creds = flow.run_local_server(
                port=0,
                access_type='offline',
                prompt='consent'
            )

        # Save credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        print("✓ Token saved to token.json")

    display_token_info(creds)
    return creds


def display_token_info(creds):
    """Display token information and GitHub Secrets setup instructions"""

    # Load the token.json to display
    with open('token.json', 'r') as f:
        token_data = json.load(f)

    print("\n" + "=" * 70)
    print("TOKEN GENERATED SUCCESSFULLY!")
    print("=" * 70)

    print("\n📋 COPY THIS ENTIRE JSON FOR GITHUB SECRETS:")
    print("-" * 70)
    print(json.dumps(token_data, indent=2))
    print("-" * 70)

    print("\n📝 NEXT STEPS:")
    print("1. Go to your GitHub repository")
    print("2. Navigate to: Settings > Secrets and variables > Actions")
    print("3. Click 'New repository secret'")
    print("4. Name: GOOGLE_TOKEN_JSON")
    print("5. Value: Copy the entire JSON above (including { and })")
    print("6. Click 'Add secret'")

    print("\n⚠️  IMPORTANT SECURITY NOTES:")
    print("- token.json contains sensitive credentials")
    print("- Never commit token.json to Git (already in .gitignore)")
    print("- Keep credentials.json private as well")
    print("- Refresh tokens can be revoked at: https://myaccount.google.com/permissions")

    print("\n" + "=" * 70)

    # Check if refresh token exists
    if not token_data.get('refresh_token'):
        print("\n⚠️  WARNING: No refresh token found!")
        print("This might happen if you previously authorized this app.")
        print("To get a refresh token:")
        print("1. Delete token.json")
        print("2. Run this script again")
        print("3. Make sure to approve the consent screen")


def test_token():
    """Test the generated token by listing Drive files"""
    try:
        from googleapiclient.discovery import build

        if not os.path.exists('token.json'):
            print("✗ No token.json found. Run generate_oauth_token() first.")
            return False

        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("✗ Token is not valid")
                return False

        service = build('drive', 'v3', credentials=creds)

        # Test by listing files (only files created by this app due to drive.file scope)
        results = service.files().list(pageSize=10, fields="files(id, name)").execute()
        files = results.get('files', [])

        print("\n✓ Token test successful!")
        print(f"→ Found {len(files)} file(s) created by this app")

        if files:
            print("\nRecent files:")
            for item in files[:5]:
                print(f"  - {item['name']} (ID: {item['id']})")

        return True

    except Exception as e:
        print(f"✗ Token test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("GOOGLE DRIVE OAUTH TOKEN GENERATOR")
    print("=" * 70)
    print()

    creds = generate_oauth_token()

    if creds:
        print("\n" + "=" * 70)
        print("Testing token...")
        print("=" * 70)
        test_token()
