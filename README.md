# Backend API Integration Testing Framework

[![API Integration Tests](https://github.com/syamsasi99/n8n-demo-backend-tests/actions/workflows/test.yml/badge.svg)](https://github.com/syamsasi99/n8n-demo-backend-tests/actions/workflows/test.yml)
[![Scheduled Tests](https://github.com/syamsasi99/n8n-demo-backend-tests/actions/workflows/scheduled-test.yml/badge.svg)](https://github.com/syamsasi99/n8n-demo-backend-tests/actions/workflows/scheduled-test.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based backend API integration testing framework built with pytest that simulates API tests with random failures for realistic testing scenarios.

## Features

- **20 Sample API Integration Tests** covering common API operations (CRUD)
- **Random Failure Simulation** - Tests randomly fail with various HTTP error codes
- **JSON Test Result Reports** - Detailed test execution reports in JSON format
- **Enhanced Reporting** - Summary statistics, failure analysis, and performance metrics
- **Fake API Client** - Simulates backend API with realistic failure scenarios
- **Pytest Markers** - Organize tests by type (api, smoke, regression)

## Project Structure

```
n8n-demo-backend-tests/
├── .github/
│   └── workflows/
│       ├── test.yml                # Main CI/CD workflow
│       ├── continuous-test.yml     # Multi-run testing workflow
│       └── scheduled-test.yml      # Scheduled monitoring workflow
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures and configuration
│   ├── fake_api_client.py          # Fake API client with random failures
│   └── test_api_integration.py     # 20 sample API tests
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
├── generate_report.py              # Enhanced report generator
├── run_tests.sh                    # Quick start script
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## Installation

### Option 1: Using Virtual Environment (Recommended)

1. **Create a virtual environment:**

```bash
python3 -m venv venv
```

2. **Activate the virtual environment:**

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Option 2: System-wide Installation

```bash
pip install -r requirements.txt
```

**Note:** Virtual environment is recommended to avoid conflicts with other Python projects.

## Quick Start

The fastest way to run tests and generate reports:

```bash
# Using the provided script (if using venv, activate it first)
./run_tests.sh

# Or manually
pytest && python generate_report.py
```

## Running Tests

### Run All Tests

```bash
pytest
```

This will:
- Execute all 20 tests
- Generate `test_results.json` with detailed results
- Display test outcomes in the terminal

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test Markers

```bash
# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression

# Run all API tests
pytest -m api
```

### Run Specific Test File

```bash
pytest tests/test_api_integration.py
```

### Run Specific Test

```bash
pytest tests/test_api_integration.py::test_create_user
```

## Generate Enhanced Report

After running tests, generate an enhanced report with detailed analysis:

```bash
python generate_report.py
```

This creates `test_report_enhanced.json` with:
- Test execution summary
- Pass/fail rates
- Detailed failure analysis
- Performance metrics
- Error categorization

## Understanding Random Failures

The framework simulates realistic API failures with a **30% failure rate** (configurable). Tests can fail with:

| Error Type | HTTP Code | Description |
|------------|-----------|-------------|
| Timeout | 408 | Request timeout |
| Internal Server Error | 500 | Server-side error |
| Bad Gateway | 502 | Invalid response from upstream |
| Service Unavailable | 503 | Service temporarily unavailable |
| Unauthorized | 401 | Authentication required |
| Forbidden | 403 | Access denied |
| Not Found | 404 | Resource not found |
| Validation Error | 422 | Request validation failed |
| Rate Limit | 429 | Too many requests |
| Conflict | 409 | Resource conflict |

### Adjusting Failure Rate

Edit the failure rate in [tests/conftest.py](tests/conftest.py#L14):

```python
@pytest.fixture(scope="function")
def api_client():
    return FakeAPIClient(failure_rate=0.3)  # Change this value (0.0 to 1.0)
```

## Sample Test Cases

The framework includes 20 comprehensive API tests:

1. **User Management (5 tests)**
   - Get user list
   - Get user by ID
   - Create user
   - Update user
   - Delete user

2. **Product Management (5 tests)**
   - Get product list
   - Get product by ID
   - Create product
   - Update product
   - Patch product price

3. **Order Management (5 tests)**
   - Get order list
   - Get order by ID
   - Create order
   - Update order status
   - Cancel order

4. **Search & Filtering (2 tests)**
   - Search products
   - Get user orders

5. **Shopping Cart (3 tests)**
   - Add product to cart
   - Get cart contents
   - Checkout cart

## Test Report Structure

### Basic Report (`test_results.json`)

Generated automatically by pytest-json-report:

```json
{
  "created": "timestamp",
  "duration": 1.23,
  "exitcode": 0,
  "tests": [
    {
      "nodeid": "tests/test_api_integration.py::test_create_user",
      "outcome": "passed",
      "duration": 0.05
    }
  ]
}
```

### Enhanced Report (`test_report_enhanced.json`)

Generated by `generate_report.py`:

```json
{
  "report_metadata": {
    "generated_at": "2025-11-06T...",
    "total_duration": 1.23
  },
  "summary": {
    "total_tests": 20,
    "passed": 14,
    "failed": 6,
    "pass_rate": 70.0,
    "fail_rate": 30.0
  },
  "test_results": {
    "passed": [...],
    "failed": [...]
  },
  "failure_analysis": {
    "error_types": {
      "Timeout": 2,
      "Service Unavailable": 3,
      "Internal Server Error": 1
    }
  },
  "performance_metrics": {
    "fastest_test": {...},
    "slowest_test": {...},
    "average_duration": 0.06
  }
}
```

## Configuration

### pytest.ini

Customize pytest behavior:

```ini
[pytest]
testpaths = tests
addopts = -v --json-report --json-report-file=test_results.json
markers =
    api: API integration tests
    smoke: Smoke tests
    regression: Regression tests
```

## Advanced Usage

### Run Tests Multiple Times

```bash
# Run tests 5 times to see different failure patterns
for i in {1..5}; do
  echo "Run $i"
  pytest
  python generate_report.py
done
```

### Collect Only (Don't Execute)

```bash
pytest --collect-only
```

### Show Test Duration

```bash
pytest --durations=10
```

### Stop on First Failure

```bash
pytest -x
```

### Run Failed Tests Only

```bash
pytest --lf
```

## Extending the Framework

### Add New Tests

Add new test functions to [tests/test_api_integration.py](tests/test_api_integration.py):

```python
@pytest.mark.api
def test_new_endpoint(api_client):
    """Test description"""
    response = api_client.get("/new-endpoint")
    assert response.status_code == 200
```

### Add New Fixtures

Add fixtures to [tests/conftest.py](tests/conftest.py):

```python
@pytest.fixture
def custom_test_data():
    return {"key": "value"}
```

### Customize Fake API Responses

Modify [tests/fake_api_client.py](tests/fake_api_client.py) to add custom response logic.

## Troubleshooting

### No Module Named 'tests'

```bash
# Ensure you're in the project root directory
cd /Users/syamsasi/code/n8n-demo-backend-tests
pytest
```

### JSON Report Not Generated

Check that pytest-json-report is installed:

```bash
pip install pytest-json-report
```

### All Tests Passing/Failing

Adjust the `failure_rate` in [tests/conftest.py](tests/conftest.py#L14).

## GitHub Actions CI/CD

The framework includes three GitHub Actions workflows for automated testing:

### 1. Standard Test Workflow ([.github/workflows/test.yml](.github/workflows/test.yml))

Runs automatically on:
- Push to `master`, `main`, or `develop` branches
- Pull requests
- Daily at 9 AM UTC
- Manual trigger via GitHub Actions UI

**Features:**
- Tests across Python 3.9, 3.10, 3.11, and 3.12
- Generates and uploads test results as artifacts
- Posts test summary to PR comments
- Displays results in GitHub job summary

**Manual Trigger:**
```bash
# Via GitHub CLI
gh workflow run test.yml
```

### 2. Continuous Testing Workflow ([.github/workflows/continuous-test.yml](.github/workflows/continuous-test.yml))

Runs multiple test iterations to analyze random failure patterns.

**Features:**
- Run 3, 5, or 10 test iterations
- Generate aggregate statistics
- Analyze test stability across runs
- Track error distribution patterns

**Manual Trigger:**
```bash
# Via GitHub CLI
gh workflow run continuous-test.yml -f runs=5
```

### 3. Scheduled Testing Workflow ([.github/workflows/scheduled-test.yml](.github/workflows/scheduled-test.yml))

Runs automatically every 6 hours to monitor test health.

**Features:**
- Automatic scheduled runs
- Alert on high failure rates (>80%)
- 7-day artifact retention
- Can be manually triggered

**Viewing Results:**
1. Go to your repository's "Actions" tab
2. Select a workflow run
3. Download artifacts or view the job summary

### Setting Up GitHub Actions

1. Push your code to GitHub:
```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin master
```

2. GitHub Actions will automatically start running on the next push or PR

3. Configure secrets if needed (none required for this framework)

### Customizing Workflows

Edit the workflow files in [.github/workflows/](.github/workflows/) to:
- Change Python versions
- Modify trigger schedules
- Adjust failure thresholds
- Add notifications (Slack, email, etc.)

## License

MIT License

## Contributing

Feel free to submit issues or pull requests to enhance the framework.