"""
Pytest configuration and fixtures for API integration tests
"""
import pytest
import random
from faker import Faker
from tests.fake_api_client import FakeAPIClient


@pytest.fixture(scope="session")
def faker_instance():
    """Provides a Faker instance for generating test data"""
    return Faker()


@pytest.fixture(scope="function")
def api_client():
    """Provides a fake API client instance with random failure simulation"""
    return FakeAPIClient(failure_rate=0.3)  # 30% chance of random failures


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
