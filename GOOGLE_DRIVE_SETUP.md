# Google Drive Upload Setup (OAuth)

This guide explains how to set up automated uploading of test reports to Google Drive using OAuth authentication.

## Overview

This setup uses **OAuth 2.0** authentication, which allows the app to upload files to your personal Google Drive account. This is the recommended approach for individual users.

## Prerequisites

- A Google account
- Access to Google Cloud Console
- Python 3.8+ installed locally

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

## Step 2: Enable Google Drive API

1. In Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Google Drive API"
3. Click **Enable**

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**
2. Choose **External** user type (unless you have a Google Workspace account)
3. Click **Create**
4. Fill in the required information:
   - **App name**: `Test Report Uploader` (or any name you prefer)
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Click **Save and Continue**
6. On the **Scopes** page, click **Add or Remove Scopes**
7. Add the following scope: `https://www.googleapis.com/auth/drive.file`
   - This allows the app to only access files it creates
8. Click **Update** and then **Save and Continue**
9. On the **Test users** page, click **Add Users**
10. Add your Google account email
11. Click **Save and Continue**

## Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Choose application type: **Desktop app**
4. Give it a name: `Test Report Uploader - Desktop`
5. Click **Create**
6. Click **Download JSON** to download the credentials
7. Save the file as `credentials.json` in your project directory

## Step 5: Generate OAuth Refresh Token (Local Setup)

**This is a one-time setup that must be done locally on your machine.**

1. Make sure `credentials.json` is in your project directory
2. Install dependencies (if not already installed):
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
3. Run the token generator script:
   ```bash
   python get_oauth_token.py
   ```
4. Your browser will automatically open for authentication:
   - Sign in with your Google account
   - Click **Continue** on the consent screen
   - Grant access to Google Drive
5. The script will generate `token.json` and display its contents
6. **Copy the entire JSON output** - you'll need it for GitHub Secrets

**Example output:**
```json
{
  "token": "ya29.a0AfH6SMB...",
  "refresh_token": "1//0gHW9Y...",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "123456789.apps.googleusercontent.com",
  "client_secret": "GOCSPX-...",
  "scopes": ["https://www.googleapis.com/auth/drive.file"]
}
```

## Step 6: Get Google Drive Folder ID

1. Open [Google Drive](https://drive.google.com/)
2. Create a folder where you want to upload test reports (or use an existing folder)
3. Open the folder
4. Copy the **Folder ID** from the URL:
   - URL format: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - The FOLDER_ID is the long string after `/folders/`
   - Example: If URL is `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h`, then Folder ID is `1a2b3c4d5e6f7g8h`

## Step 7: Configure GitHub Secrets

1. In your GitHub repository, go to **Settings > Secrets and variables > Actions**
2. Click **New repository secret**
3. Add the following secrets:

   **GOOGLE_TOKEN_JSON**
   - Name: `GOOGLE_TOKEN_JSON`
   - Value: Paste the **entire JSON output** from Step 5
   - Click **Add secret**

   **GOOGLE_DRIVE_FOLDER_ID** (Optional)
   - Name: `GOOGLE_DRIVE_FOLDER_ID`
   - Value: Paste the folder ID from Step 6
   - Click **Add secret**
   - Note: If not provided, files will be uploaded to your Drive's root folder

## Step 8: Test Locally (Optional)

For local testing before pushing to GitHub:

```bash
# Set environment variables (Linux/Mac)
export GOOGLE_TOKEN_JSON='{"token":"ya29...","refresh_token":"1//0g...",...}'
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id-here"

# Or simply use the token.json file that was generated
python upload_to_drive.py --file test_report_enhanced.json --credentials token.json --folder-id "your-folder-id"
```

```powershell
# Set environment variables (Windows PowerShell)
$env:GOOGLE_TOKEN_JSON='{"token":"ya29...","refresh_token":"1//0g...",...}'
$env:GOOGLE_DRIVE_FOLDER_ID="your-folder-id-here"

# Or use the token.json file
python upload_to_drive.py --file test_report_enhanced.json --credentials token.json --folder-id "your-folder-id"
```

## Uploaded File Naming Convention

Files uploaded to Google Drive will have the following format:

```
test_report_YYYY-MM-DD_HH-MM-SS_run_RUN_ID_(XP_YF_ZT).json
```

Where:
- `YYYY-MM-DD_HH-MM-SS`: Timestamp of report generation
- `RUN_ID`: GitHub Actions run ID or "local" for local runs
- `XP`: Number of passed tests
- `YF`: Number of failed tests
- `ZT`: Total number of tests

Example:
```
test_report_2025-01-15_14-30-45_run_12345678_(15P_5F_20T).json
```

## Security Best Practices

1. **Never commit sensitive files to Git**
   - `credentials.json` - OAuth client secrets (already in `.gitignore`)
   - `token.json` - OAuth tokens with refresh token (already in `.gitignore`)
   - These are already excluded in `.gitignore`

2. **Rotate OAuth tokens periodically**
   - Refresh tokens can be revoked at: [Google Account Permissions](https://myaccount.google.com/permissions)
   - Regenerate tokens every 3-6 months for security

3. **Use minimal permissions**
   - We use `drive.file` scope which only allows access to files created by this app
   - This is safer than full Drive access

4. **Protect GitHub Secrets**
   - Only repository admins should have access to secrets
   - Never log or expose the GOOGLE_TOKEN_JSON value

5. **Monitor usage**
   - Check [Google Cloud Console](https://console.cloud.google.com/apis/api/drive.googleapis.com) for API usage
   - Review uploaded files in your Drive folder periodically

## Troubleshooting

### "Invalid credentials" Error
- Make sure you copied the entire `token.json` contents to GitHub Secrets
- Verify the JSON is valid (no missing brackets or quotes)
- Ensure you included the `refresh_token` field

### "No refresh token available" Error
- This happens if you didn't use `access_type='offline'` during token generation
- Solution: Delete `token.json` and run `get_oauth_token.py` again
- Make sure to approve the consent screen when prompted

### Browser doesn't open during token generation
- Make sure you're running `get_oauth_token.py` on your local machine (not on a server)
- If using SSH, forward the port: `ssh -L 8080:localhost:8080 user@server`
- Manually copy the URL from the terminal and open it in your browser

### "App is not published" Warning
- This is normal when using "External" user type in testing mode
- Click "Advanced" → "Go to [App Name] (unsafe)" to proceed
- This is safe for your own app

### Token expires / Invalid grant
- Refresh tokens can expire after 6 months of inactivity
- Regenerate the token by running `get_oauth_token.py` again
- Update the GitHub Secret with the new token

### Files uploaded to root instead of specific folder
- Verify you set the `GOOGLE_DRIVE_FOLDER_ID` secret correctly
- Double-check the folder ID from the Drive URL
- Make sure your Google account owns the folder or has access to it

## Additional Resources

- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)
- [Service Account Documentation](https://cloud.google.com/iam/docs/service-accounts)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
