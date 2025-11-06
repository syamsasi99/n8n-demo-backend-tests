# Google Drive Upload Setup

This guide explains how to set up automated uploading of test reports to Google Drive.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

## Step 2: Enable Google Drive API

1. In Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Google Drive API"
3. Click **Enable**

## Step 3: Create a Service Account

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > Service Account**
3. Fill in the details:
   - Service account name: `test-report-uploader`
   - Service account ID: `test-report-uploader`
   - Description: `Uploads test reports to Google Drive`
4. Click **Create and Continue**
5. Skip the optional steps and click **Done**

## Step 4: Create Service Account Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key > Create New Key**
4. Select **JSON** format
5. Click **Create**
6. The JSON key file will be downloaded - **keep this file secure!**

## Step 5: Share Google Drive Folder with Service Account

1. Create a folder in Google Drive where you want to upload test reports
2. Right-click the folder and select **Share**
3. Enter the service account email (found in the JSON key file or Cloud Console)
   - Format: `test-report-uploader@YOUR-PROJECT-ID.iam.gserviceaccount.com`
4. Give it **Editor** access
5. Copy the folder ID from the URL:
   - URL format: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - The FOLDER_ID is the long string after `/folders/`

## Step 6: Configure GitHub Secrets (for CI/CD)

1. In your GitHub repository, go to **Settings > Secrets and variables > Actions**
2. Add the following secrets:

   **GOOGLE_DRIVE_CREDENTIALS**
   - Click **New repository secret**
   - Name: `GOOGLE_DRIVE_CREDENTIALS`
   - Value: Paste the entire contents of the JSON key file
   - Click **Add secret**

   **GOOGLE_DRIVE_FOLDER_ID**
   - Click **New repository secret**
   - Name: `GOOGLE_DRIVE_FOLDER_ID`
   - Value: Paste the folder ID from Step 5
   - Click **Add secret**

## Step 7: Local Testing (Optional)

For local testing, set environment variables:

```bash
# Linux/Mac
export GOOGLE_DRIVE_CREDENTIALS="/path/to/service-account-key.json"
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id-here"

# Windows (PowerShell)
$env:GOOGLE_DRIVE_CREDENTIALS="C:\path\to\service-account-key.json"
$env:GOOGLE_DRIVE_FOLDER_ID="your-folder-id-here"
```

Then run tests and upload:

```bash
# Run tests
pytest -v

# Generate enhanced report
python generate_report.py

# Upload to Google Drive
python upload_to_drive.py
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

1. **Never commit the service account JSON key to Git**
   - Already added to `.gitignore` as `*credentials*.json`

2. **Rotate keys periodically**
   - Create a new key and delete the old one every few months

3. **Use minimal permissions**
   - Service account only has access to the specific folder
   - Only has Editor permissions (not Owner)

4. **Monitor usage**
   - Check Google Cloud Console for API usage
   - Review uploaded files periodically

## Troubleshooting

### Authentication Error
- Verify the service account JSON is correct
- Ensure the service account has access to the folder
- Check that Google Drive API is enabled

### Folder Not Found
- Verify the folder ID is correct
- Make sure you shared the folder with the service account email
- Check that the service account has Editor permissions

### Quota Exceeded
- Google Drive API has usage quotas
- Check [Google Cloud Console](https://console.cloud.google.com/apis/api/drive.googleapis.com/quotas) for limits
- Default limit: 20,000 requests per 100 seconds per user

## Additional Resources

- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)
- [Service Account Documentation](https://cloud.google.com/iam/docs/service-accounts)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
