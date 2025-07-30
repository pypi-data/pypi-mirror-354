"""Tests for the models module."""

import pytest
from pydantic import ValidationError

from lightwave_ai.core.models import APIRequest, APIResponse, ErrorResponse


@pytest.mark.unit
class TestAPIModels:
    """Tests for the API models."""
    
    def test_api_request_validation(self):
        """Test that API request validates correctly."""
        # Valid request
        request = APIRequest(prompt="Test prompt")
        assert request.prompt == "Test prompt"
        
        # Test required fields
        with pytest.raises(ValidationError):
            APIRequest()  # prompt is required
    
    def test_api_response_model(self):
        """Test the API response model."""
        response = APIResponse(
            response="Test response",
            request_id="123",
            model="test-model",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        )
        
        assert response.response == "Test response"
        assert response.request_id == "123"
        assert response.model == "test-model"
        assert response.usage["prompt_tokens"] == 10
        assert response.usage["completion_tokens"] == 20
        assert response.usage["total_tokens"] == 30
    
    def test_error_response_model(self):
        """Test the error response model."""
        error = ErrorResponse(
            error="Test error",
            error_code="TEST_ERROR",
            detail="Test error detail",
            request_id="123"
        )
        
        assert error.error == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.detail == "Test error detail"
        assert error.request_id == "123"
        
        # Test model dictionary conversion
        error_dict = error.model_dump()
        assert error_dict["error"] == "Test error"
        assert error_dict["error_code"] == "TEST_ERROR"
        assert error_dict["detail"] == "Test error detail"
        assert error_dict["request_id"] == "123" 