"""
Upload test results to Google Drive
"""
import os
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


class DriveUploader:
    """Upload files to Google Drive"""

    def __init__(self, credentials_path=None, folder_id=None):
        """
        Initialize Drive uploader

        Args:
            credentials_path: Path to service account credentials JSON
            folder_id: Google Drive folder ID to upload to
        """
        self.credentials_path = credentials_path or os.getenv('GOOGLE_DRIVE_CREDENTIALS')
        self.folder_id = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.service = None

    def authenticate(self):
        """Authenticate with Google Drive API"""
        try:
            if not self.credentials_path:
                raise ValueError("Google Drive credentials path not provided. Set GOOGLE_DRIVE_CREDENTIALS environment variable.")

            # Use service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )

            self.service = build('drive', 'v3', credentials=credentials)
            print("✓ Successfully authenticated with Google Drive")
            return True

        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            return False

    def upload_file(self, file_path, custom_name=None):
        """
        Upload a file to Google Drive

        Args:
            file_path: Path to file to upload
            custom_name: Optional custom name for the file in Drive

        Returns:
            File ID if successful, None otherwise
        """
        if not self.service:
            if not self.authenticate():
                return None

        try:
            file_name = custom_name or os.path.basename(file_path)

            file_metadata = {
                'name': file_name
            }

            # If folder ID is specified, upload to that folder
            if self.folder_id:
                file_metadata['parents'] = [self.folder_id]

            media = MediaFileUpload(
                file_path,
                mimetype='application/json',
                resumable=True
            )

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            print(f"✓ Uploaded: {file.get('name')}")
            print(f"  File ID: {file.get('id')}")
            print(f"  Link: {file.get('webViewLink')}")

            return file.get('id')

        except HttpError as error:
            print(f"✗ Upload failed: {error}")
            return None


def main():
    """Main function to upload test report"""
    import argparse

    parser = argparse.ArgumentParser(description='Upload test report to Google Drive')
    parser.add_argument('--file', default='test_report_enhanced.json', help='File to upload')
    parser.add_argument('--credentials', help='Path to Google Drive credentials JSON')
    parser.add_argument('--folder-id', help='Google Drive folder ID')
    parser.add_argument('--run-id', help='GitHub run ID or custom run identifier')
    args = parser.parse_args()

    # Check if file exists
    if not os.path.exists(args.file):
        print(f"✗ File not found: {args.file}")
        return 1

    # Load the report to get metadata
    try:
        with open(args.file, 'r') as f:
            report = json.load(f)
    except Exception as e:
        print(f"✗ Failed to read report: {e}")
        return 1

    # Generate filename with timestamp and run ID
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    run_id = args.run_id or os.getenv('GITHUB_RUN_ID', 'local')

    # Include test summary in filename
    summary = report.get('summary', {})
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    total = summary.get('total_tests', 0)

    custom_name = f"test_report_{timestamp}_run_{run_id}_({passed}P_{failed}F_{total}T).json"

    print("=" * 60)
    print("GOOGLE DRIVE UPLOADER")
    print("=" * 60)
    print(f"File: {args.file}")
    print(f"Upload Name: {custom_name}")
    print(f"Run ID: {run_id}")
    print(f"Test Summary: {passed} passed, {failed} failed, {total} total")
    print("=" * 60)

    # Upload to Google Drive
    uploader = DriveUploader(
        credentials_path=args.credentials,
        folder_id=args.folder_id
    )

    file_id = uploader.upload_file(args.file, custom_name)

    if file_id:
        print("=" * 60)
        print("✓ Upload successful!")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("✗ Upload failed!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
