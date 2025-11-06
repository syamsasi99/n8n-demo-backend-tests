"""
Pytest configuration and fixtures for API integration tests
"""
import pytest
import random
import json
from faker import Faker
from tests.fake_api_client import FakeAPIClient, APIException


@pytest.fixture(scope="session")
def faker_instance():
    """Provides a Faker instance for generating test data"""
    return Faker()


@pytest.fixture(scope="function")
def api_client(request):
    """Provides a fake API client instance with random failure simulation"""
    client = FakeAPIClient(failure_rate=0.3)  # 30% chance of random failures

    # Store reference to request for log capturing
    client._test_request = request

    return client


@pytest.fixture(scope="function")
def test_user_data(faker_instance):
    """Generates fake user data for testing"""
    return {
        "id": random.randint(1, 10000),
        "username": faker_instance.user_name(),
        "email": faker_instance.email(),
        "first_name": faker_instance.first_name(),
        "last_name": faker_instance.last_name(),
        "phone": faker_instance.phone_number(),
        "address": faker_instance.address()
    }


@pytest.fixture(scope="function")
def test_product_data(faker_instance):
    """Generates fake product data for testing"""
    return {
        "id": random.randint(1, 1000),
        "name": faker_instance.catch_phrase(),
        "description": faker_instance.text(),
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(0, 500),
        "category": random.choice(["Electronics", "Clothing", "Books", "Home", "Sports"])
    }


@pytest.fixture(scope="function")
def test_order_data(faker_instance):
    """Generates fake order data for testing"""
    return {
        "id": random.randint(1, 50000),
        "user_id": random.randint(1, 10000),
        "items": [
            {
                "product_id": random.randint(1, 1000),
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(10.0, 500.0), 2)
            }
            for _ in range(random.randint(1, 5))
        ],
        "total": round(random.uniform(50.0, 5000.0), 2),
        "status": random.choice(["pending", "processing", "shipped", "delivered"])
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture API logs and attach them to test reports
    """
    outcome = yield
    report = outcome.get_result()

    # Only process during the call phase (actual test execution)
    if report.when == "call":
        # Initialize logs list if not present
        if not hasattr(report, "logs"):
            report.logs = []

        # Try to extract logs from the test execution
        # Logs can come from successful API responses or exceptions
        if hasattr(call, "excinfo") and call.excinfo is not None:
            # Test failed - check if it's an APIException with logs
            exc_value = call.excinfo.value
            if isinstance(exc_value, APIException) and hasattr(exc_value, "logs"):
                report.logs.append(exc_value.logs)
                # Also store the error details
                report.api_error = {
                    "status_code": exc_value.status_code,
                    "message": exc_value.message,
                    "logs": exc_value.logs
                }

        # For successful tests, try to capture logs from response objects
        # stored in test instance variables
        if hasattr(item, "funcargs"):
            for arg_name, arg_value in item.funcargs.items():
                # Check if any fixture returned a response with logs
                if hasattr(arg_value, "logs"):
                    report.logs.append(arg_value.logs)


def pytest_json_modifyreport(json_report):
    """
    Modify the JSON report to include API logs
    """
    for test in json_report.get("tests", []):
        if hasattr(test, "logs"):
            test["api_logs"] = test.logs
        if hasattr(test, "api_error"):
            test["api_error"] = test.api_error
