"""
Fake API Client that simulates backend API responses with random failures
"""
import random
import time
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from faker import Faker

fake = Faker()


class APIException(Exception):
    """Custom exception for API errors"""
    def __init__(self, status_code: int, message: str, logs: Dict = None):
        self.status_code = status_code
        self.message = message
        self.logs = logs or {}
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
        self._test_request = None  # Will be set by fixture

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

    def _generate_logs(self, method: str, endpoint: str, data: Any, status_code: int, duration: float, is_error: bool = False) -> Dict:
        """
        Generates detailed fake logs for API request/response

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request/response data
            status_code: HTTP status code
            duration: Request duration in seconds
            is_error: Whether this is an error response

        Returns:
            Dictionary containing detailed logs
        """
        request_id = fake.uuid4()
        timestamp = datetime.now().isoformat()

        logs = {
            "request": {
                "request_id": request_id,
                "timestamp": timestamp,
                "method": method,
                "url": f"{self.base_url}{endpoint}",
                "headers": {
                    "User-Agent": fake.user_agent(),
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-Request-ID": request_id,
                    "X-Correlation-ID": fake.uuid4(),
                    "Authorization": f"Bearer {fake.sha256()[:32]}"
                },
                "body": data if data else None,
                "client_ip": fake.ipv4(),
                "duration_ms": round(duration * 1000, 2)
            },
            "response": {
                "status_code": status_code,
                "headers": {
                    "Content-Type": "application/json",
                    "X-Response-Time": f"{round(duration * 1000, 2)}ms",
                    "X-Request-ID": request_id,
                    "Server": f"{fake.company()}-API/1.{random.randint(0, 9)}.{random.randint(0, 20)}",
                    "X-RateLimit-Limit": "1000",
                    "X-RateLimit-Remaining": str(random.randint(100, 999)),
                    "Date": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
                },
                "body": data if not is_error else None
            },
            "server_logs": []
        }

        # Add detailed server-side logs
        if is_error:
            error_trace = self._generate_error_trace(status_code)
            logs["server_logs"].extend(error_trace)
        else:
            logs["server_logs"].extend(self._generate_success_logs(method, endpoint))

        # Add performance metrics
        logs["performance"] = {
            "db_query_time_ms": round(random.uniform(5, 50), 2),
            "cache_hit": random.choice([True, False]),
            "upstream_call_time_ms": round(random.uniform(10, 100), 2),
            "total_time_ms": round(duration * 1000, 2)
        }

        # Add connection details
        logs["connection"] = {
            "remote_addr": fake.ipv4(),
            "server_addr": fake.ipv4_private(),
            "port": random.choice([80, 443, 8080, 8443]),
            "protocol": "HTTP/1.1",
            "tls_version": random.choice(["TLSv1.2", "TLSv1.3"]) if random.choice([True, False]) else None
        }

        return logs

    def _generate_error_trace(self, status_code: int) -> List[Dict]:
        """Generates fake error stack trace and logs"""
        traces = []

        # Initial error log
        traces.append({
            "level": "ERROR",
            "timestamp": datetime.now().isoformat(),
            "message": f"Request failed with status {status_code}",
            "logger": "api.request_handler"
        })

        # Fake stack trace based on error type
        if status_code >= 500:
            traces.append({
                "level": "ERROR",
                "timestamp": datetime.now().isoformat(),
                "message": f"Exception in thread 'http-nio-8080-exec-{random.randint(1, 100)}'",
                "logger": "server.handler",
                "exception": {
                    "type": random.choice(["DatabaseConnectionError", "TimeoutException", "NullPointerException", "ServiceUnavailableException"]),
                    "message": fake.sentence(),
                    "stack_trace": [
                        f"at com.api.service.{fake.word()}.{fake.word()}({fake.file_name(extension='java')}:{random.randint(1, 500)})",
                        f"at com.api.controller.{fake.word()}.handle({fake.file_name(extension='java')}:{random.randint(1, 300)})",
                        f"at com.framework.dispatcher.dispatch({fake.file_name(extension='java')}:{random.randint(1, 200)})"
                    ]
                }
            })

            # Database error for 500s
            traces.append({
                "level": "ERROR",
                "timestamp": datetime.now().isoformat(),
                "message": f"Database query failed: Connection timeout after {random.randint(5000, 30000)}ms",
                "logger": "database.connection",
                "query": f"SELECT * FROM {fake.word()} WHERE id = {random.randint(1, 10000)}"
            })

        elif status_code == 401 or status_code == 403:
            traces.append({
                "level": "WARN",
                "timestamp": datetime.now().isoformat(),
                "message": "Authentication failed: Invalid or expired token",
                "logger": "security.auth",
                "details": {
                    "token_expired": random.choice([True, False]),
                    "invalid_signature": random.choice([True, False]),
                    "user_id": None
                }
            })

        elif status_code == 404:
            traces.append({
                "level": "WARN",
                "timestamp": datetime.now().isoformat(),
                "message": f"Resource not found in database",
                "logger": "database.repository",
                "query": f"SELECT * FROM {fake.word()} WHERE id = {random.randint(1, 10000)}"
            })

        elif status_code == 422:
            traces.append({
                "level": "WARN",
                "timestamp": datetime.now().isoformat(),
                "message": "Validation failed",
                "logger": "validator.schema",
                "validation_errors": [
                    {
                        "field": random.choice(["email", "name", "price", "quantity", "date"]),
                        "error": random.choice(["required", "invalid_format", "out_of_range", "too_long"])
                    }
                ]
            })

        elif status_code == 429:
            traces.append({
                "level": "WARN",
                "timestamp": datetime.now().isoformat(),
                "message": "Rate limit exceeded",
                "logger": "middleware.ratelimit",
                "details": {
                    "limit": 1000,
                    "window": "1 hour",
                    "current_count": random.randint(1000, 1500),
                    "reset_at": datetime.now().isoformat()
                }
            })

        return traces

    def _generate_success_logs(self, method: str, endpoint: str) -> List[Dict]:
        """Generates fake success logs"""
        logs = []

        logs.append({
            "level": "INFO",
            "timestamp": datetime.now().isoformat(),
            "message": f"{method} {endpoint} - Request received",
            "logger": "api.request_handler"
        })

        logs.append({
            "level": "DEBUG",
            "timestamp": datetime.now().isoformat(),
            "message": f"Database query executed successfully",
            "logger": "database.repository",
            "query_time_ms": round(random.uniform(5, 50), 2)
        })

        if method in ["POST", "PUT", "PATCH"]:
            logs.append({
                "level": "INFO",
                "timestamp": datetime.now().isoformat(),
                "message": f"Resource {'created' if method == 'POST' else 'updated'} successfully",
                "logger": "service.handler",
                "resource_id": random.randint(1, 10000)
            })

        logs.append({
            "level": "INFO",
            "timestamp": datetime.now().isoformat(),
            "message": f"{method} {endpoint} - Request completed successfully",
            "logger": "api.request_handler"
        })

        return logs

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
        start_time = time.time()
        self._simulate_delay()
        duration = time.time() - start_time

        # Randomly fail based on failure rate
        if self._should_fail():
            failure = self._get_random_failure()
            logs = self._generate_logs(method, endpoint, data, failure["code"], duration, is_error=True)

            # Store logs in pytest metadata if available
            if self._test_request:
                try:
                    self._test_request.node.user_properties.append(("logs", logs))
                except:
                    pass  # If pytest context not available, ignore

            raise APIException(failure["code"], failure["message"], logs)

        # Simulate successful responses based on method
        if method == "GET":
            status_code = 200
            response_data = data or {"status": "success", "data": []}
        elif method == "POST":
            status_code = 201
            response_data = data or {"status": "created", "id": random.randint(1, 10000)}
        elif method == "PUT":
            status_code = 200
            response_data = data or {"status": "updated"}
        elif method == "DELETE":
            status_code = 204
            response_data = None
        elif method == "PATCH":
            status_code = 200
            response_data = data or {"status": "patched"}
        else:
            status_code = 200
            response_data = data or {"status": "success"}

        # Generate logs for successful request
        logs = self._generate_logs(method, endpoint, data, status_code, duration, is_error=False)

        # Store logs in pytest metadata if available
        if self._test_request:
            try:
                self._test_request.node.user_properties.append(("logs", logs))
            except:
                pass  # If pytest context not available, ignore

        # Create response with logs attached
        response = APIResponse(status_code, response_data)
        response.logs = logs  # Attach logs to response
        return response

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
