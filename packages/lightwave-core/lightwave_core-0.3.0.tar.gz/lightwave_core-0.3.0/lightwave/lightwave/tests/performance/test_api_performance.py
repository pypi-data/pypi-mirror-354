"""Performance tests for API endpoints."""

import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from lightwave_ai.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.mark.performance
class TestAPIPerformance:
    """Performance tests for API endpoints."""
    
    def test_health_endpoint_performance(self, client):
        """Test the performance of the health endpoint."""
        # Measure the time for a single request
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Check that the request was processed in under 50ms
        response_time = (end_time - start_time) * 1000  # Convert to ms
        assert response_time < 50, f"Response time was {response_time}ms, which exceeds the 50ms limit"
    
    def test_concurrent_requests(self, client):
        """Test the performance of concurrent requests."""
        num_requests = 10
        
        def make_request():
            """Make a request to the health endpoint."""
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": (end_time - start_time) * 1000  # Convert to ms
            }
        
        # Make concurrent requests
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            results = list(executor.map(lambda _: make_request(), range(num_requests)))
        
        # Check that all requests were successful
        assert all(result["status_code"] == 200 for result in results)
        
        # Calculate average response time
        avg_response_time = sum(result["response_time"] for result in results) / num_requests
        
        # Check that the average response time is under 100ms
        assert avg_response_time < 100, f"Average response time was {avg_response_time}ms, which exceeds the 100ms limit"
    
    @pytest.mark.slow
    def test_api_load(self, client):
        """Test the API under load."""
        num_requests = 50
        
        def make_request():
            """Make a request to the health endpoint."""
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": (end_time - start_time) * 1000  # Convert to ms
            }
        
        # Make concurrent requests
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            results = list(executor.map(lambda _: make_request(), range(num_requests)))
        
        # Check that all requests were successful
        assert all(result["status_code"] == 200 for result in results)
        
        # Calculate average response time
        avg_response_time = sum(result["response_time"] for result in results) / num_requests
        
        # Output performance statistics
        print(f"Average response time: {avg_response_time:.2f}ms")
        print(f"Min response time: {min(result['response_time'] for result in results):.2f}ms")
        print(f"Max response time: {max(result['response_time'] for result in results):.2f}ms") 