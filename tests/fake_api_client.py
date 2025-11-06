"""
Fake API Client that simulates backend API responses with random failures
"""
import random
import time
from typing import Dict, Any, List, Optional


class APIException(Exception):
    """Custom exception for API errors"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class APIResponse:
    """Simulates an HTTP response"""
    def __init__(self, status_code: int, data: Any = None, headers: Dict = None):
        self.status_code = status_code
        self.data = data
        self.headers = headers or {"Content-Type": "application/json"}

    def json(self):
        return self.data

    @property
    def ok(self):
        return 200 <= self.status_code < 300


class FakeAPIClient:
    """
    Simulates a backend API client with random failures
    """

    FAILURE_SCENARIOS = [
        {"type": "timeout", "message": "Request timeout", "code": 408},
        {"type": "server_error", "message": "Internal server error", "code": 500},
        {"type": "bad_gateway", "message": "Bad gateway", "code": 502},
        {"type": "service_unavailable", "message": "Service unavailable", "code": 503},
        {"type": "unauthorized", "message": "Unauthorized access", "code": 401},
        {"type": "forbidden", "message": "Forbidden", "code": 403},
        {"type": "not_found", "message": "Resource not found", "code": 404},
        {"type": "validation_error", "message": "Validation failed", "code": 422},
        {"type": "rate_limit", "message": "Rate limit exceeded", "code": 429},
        {"type": "conflict", "message": "Resource conflict", "code": 409},
    ]

    def __init__(self, base_url: str = "https://api.fake.com", failure_rate: float = 0.3):
        """
        Initialize the fake API client

        Args:
            base_url: Base URL for the API
            failure_rate: Probability of random failures (0.0 to 1.0)
        """
        self.base_url = base_url
        self.failure_rate = failure_rate
        self.request_count = 0

    def _should_fail(self) -> bool:
        """Determines if this request should fail randomly"""
        return random.random() < self.failure_rate

    def _simulate_delay(self):
        """Simulates network delay"""
        delay = random.uniform(0.01, 0.1)
        time.sleep(delay)

    def _get_random_failure(self) -> Dict:
        """Returns a random failure scenario"""
        return random.choice(self.FAILURE_SCENARIOS)

    def _make_request(self, method: str, endpoint: str, data: Any = None) -> APIResponse:
        """
        Simulates making an API request

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint
            data: Request payload

        Returns:
            APIResponse object

        Raises:
            APIException: If the request fails
        """
        self.request_count += 1
        self._simulate_delay()

        # Randomly fail based on failure rate
        if self._should_fail():
            failure = self._get_random_failure()
            raise APIException(failure["code"], failure["message"])

        # Simulate successful responses based on method
        if method == "GET":
            return APIResponse(200, data or {"status": "success", "data": []})
        elif method == "POST":
            return APIResponse(201, data or {"status": "created", "id": random.randint(1, 10000)})
        elif method == "PUT":
            return APIResponse(200, data or {"status": "updated"})
        elif method == "DELETE":
            return APIResponse(204, None)
        elif method == "PATCH":
            return APIResponse(200, data or {"status": "patched"})
        else:
            return APIResponse(200, data or {"status": "success"})

    def get(self, endpoint: str, params: Dict = None) -> APIResponse:
        """GET request"""
        return self._make_request("GET", endpoint, params)

    def post(self, endpoint: str, data: Dict = None) -> APIResponse:
        """POST request"""
        return self._make_request("POST", endpoint, data)

    def put(self, endpoint: str, data: Dict = None) -> APIResponse:
        """PUT request"""
        return self._make_request("PUT", endpoint, data)

    def delete(self, endpoint: str) -> APIResponse:
        """DELETE request"""
        return self._make_request("DELETE", endpoint)

    def patch(self, endpoint: str, data: Dict = None) -> APIResponse:
        """PATCH request"""
        return self._make_request("PATCH", endpoint, data)
