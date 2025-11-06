# GitHub Actions Setup Guide

## Overview

This project includes three automated GitHub Actions workflows for comprehensive API integration testing.

## Workflows

### 1. Main Test Workflow (`test.yml`)

**Purpose:** Primary CI/CD pipeline for pull requests and pushes

**Triggers:**
- Push to `master`, `main`, or `develop` branches
- Pull requests to these branches
- Daily at 9 AM UTC
- Manual dispatch

**What it does:**
1. Runs tests on Python 3.9, 3.10, 3.11, and 3.12
2. Generates JSON test reports
3. Uploads test artifacts
4. Posts test summary to PR comments (for PRs)
5. Displays results in GitHub job summary

**Artifacts:**
- `test-results-python-{version}`: Test results for each Python version
- Retention: 30 days

---

### 2. Continuous Testing Workflow (`continuous-test.yml`)

**Purpose:** Analyze random failure patterns across multiple test runs

**Triggers:**
- Manual dispatch only
- Choose 3, 5, or 10 test iterations

**What it does:**
1. Runs tests multiple times in sequence
2. Collects results from all runs
3. Generates aggregate statistics:
   - Average/min/max pass rates
   - Error type distribution
   - Individual test stability metrics
4. Creates comprehensive analysis report

**Artifacts:**
- `continuous-test-results`: All test runs and aggregate statistics
- Retention: 30 days

**Use cases:**
- Validate random failure simulation
- Analyze test flakiness
- Study error distribution patterns
- Assess overall framework behavior

---

### 3. Scheduled Testing Workflow (`scheduled-test.yml`)

**Purpose:** Continuous health monitoring

**Triggers:**
- Every 6 hours automatically
- Manual dispatch

**What it does:**
1. Runs complete test suite
2. Generates test reports
3. Alerts if failure rate exceeds 80%
4. Uploads results for trending analysis

**Artifacts:**
- `scheduled-test-results-{run_number}`: Test results with run number
- Retention: 7 days

**Use cases:**
- Monitor test environment health
- Track failure trends over time
- Early detection of issues

---

## Setup Instructions

### 1. Push to GitHub

```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin master
```

### 2. Enable Actions

GitHub Actions are automatically enabled for public repositories. For private repos:
1. Go to repository Settings
2. Click "Actions" in left sidebar
3. Enable "Allow all actions"

### 3. Update Badge URLs (Optional)

In `README.md`, replace `YOUR_USERNAME` with your actual GitHub username:

```markdown
[![API Integration Tests](https://github.com/YOUR_USERNAME/n8n-demo-backend-tests/actions/workflows/test.yml/badge.svg)]
```

### 4. Verify Workflows

1. Go to repository's "Actions" tab
2. Verify all three workflows are listed
3. Manually trigger a workflow to test

---

## Using the Workflows

### Manual Workflow Triggers

**Via GitHub UI:**
1. Go to "Actions" tab
2. Select workflow from left sidebar
3. Click "Run workflow"
4. Choose options (if applicable)
5. Click "Run workflow" button

**Via GitHub CLI:**

```bash
# Main test workflow
gh workflow run test.yml

# Continuous testing with 5 runs
gh workflow run continuous-test.yml -f runs=5

# Scheduled test
gh workflow run scheduled-test.yml
```

### Viewing Results

**In Pull Requests:**
- Test results automatically commented on PR
- Click "Details" next to status checks

**In Actions Tab:**
1. Click on workflow run
2. View job summary
3. Download artifacts
4. Check logs for details

**Downloading Artifacts:**

```bash
# List artifacts for a run
gh run view <run-id>

# Download artifacts
gh run download <run-id>
```

---

## Workflow Customization

### Change Python Versions

Edit `.github/workflows/test.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']  # Add/remove versions
```

### Change Schedule

Edit cron expressions:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Cron format: minute hour day month weekday
  # Examples:
  # '0 0 * * *'    - Daily at midnight
  # '0 */4 * * *'  - Every 4 hours
  # '0 9 * * 1'    - Every Monday at 9 AM
```

### Adjust Failure Threshold

Edit `.github/workflows/scheduled-test.yml`:

```yaml
if fail_rate > 80:  # Change threshold
```

### Add Notifications

Add notification steps (Slack, email, etc.):

```yaml
- name: Send Slack notification
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Tests failed in ${{ github.repository }}"
      }
```

---

## Troubleshooting

### Workflows Not Running

**Check:**
1. Workflows enabled in repository settings
2. YAML syntax is valid
3. Branch names match trigger conditions
4. No syntax errors in workflow files

**Validate locally:**
```bash
.github/validate_workflows.sh
```

### Permission Errors

For private repos, ensure:
1. Repository has Actions enabled
2. Workflow has necessary permissions
3. GITHUB_TOKEN has required scopes

### Artifacts Not Uploading

Check:
- Artifact paths are correct
- Files exist at specified paths
- Retention days within limits (1-90)

### PR Comments Not Posting

Requires:
- `pull_request` trigger
- `actions/github-script@v7` action
- Proper GITHUB_TOKEN permissions

---

## Best Practices

1. **Branch Protection:**
   - Require status checks to pass
   - Configure in Settings > Branches

2. **Artifact Management:**
   - Shorter retention for frequent runs
   - Longer retention for release builds

3. **Caching:**
   - Already configured for pip packages
   - Reduces workflow execution time

4. **Matrix Testing:**
   - Test on multiple Python versions
   - Catch version-specific issues

5. **Manual Triggers:**
   - Use for ad-hoc testing
   - Useful during development

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub CLI](https://cli.github.com/)

---

## Status Monitoring

Monitor workflow health:
1. Add status badges to README
2. Enable email notifications
3. Review workflow run history
4. Check artifact retention

**Status Badge URLs:**
```markdown
![Workflow Status](https://github.com/{owner}/{repo}/actions/workflows/{workflow}.yml/badge.svg)
```
