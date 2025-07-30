"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from lightwave_ai.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.mark.integration
class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    def test_health_endpoint(self, client):
        """Test that the health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_readiness_endpoint(self, client):
        """Test that the readiness endpoint returns 200."""
        response = client.get("/readiness")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"


@pytest.mark.integration
class TestAPIEndpoints:
    """Tests for API endpoints."""
    
    def test_api_version_endpoint(self, client):
        """Test that the API version endpoint returns correct information."""
        response = client.get("/api/v1/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "api_version" in data
        
    def test_unauthorized_access(self, client):
        """Test that protected endpoints return 401 without API key."""
        response = client.post("/api/v1/ai/generate")
        assert response.status_code == 401
        
    def test_api_docs_endpoint(self, client):
        """Test that the API docs endpoint returns 200."""
        response = client.get("/docs")
        assert response.status_code == 200 