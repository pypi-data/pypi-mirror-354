"""Demonstrates parametrized tests with pytest."""

import pytest
from lightwave_ai.core.errors import (
    APIError, BadRequestError, AuthenticationError, 
    RateLimitError, ServiceUnavailableError
)


@pytest.mark.unit
class TestErrorTypes:
    """Tests for the error types using parameterization."""
    
    @pytest.mark.parametrize(
        "error_class,status_code,error_code",
        [
            (APIError, 500, "API_ERROR"),
            (BadRequestError, 400, "BAD_REQUEST"),
            (AuthenticationError, 401, "AUTHENTICATION_ERROR"),
            (RateLimitError, 429, "RATE_LIMIT_EXCEEDED"),
            (ServiceUnavailableError, 503, "SERVICE_UNAVAILABLE"),
        ],
    )
    def test_error_attributes(self, error_class, status_code, error_code):
        """Test that errors have the correct attributes."""
        error = error_class("Test error message")
        
        assert error.status_code == status_code
        assert error.error_code == error_code
        assert str(error) == "Test error message"
        
        # Test with additional details
        error_with_details = error_class("Test error message", detail="Additional details")
        assert error_with_details.detail == "Additional details"


@pytest.mark.unit
class TestParametrizedCalculations:
    """Demonstrates different ways to use parametrized tests."""
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_addition(self, a, b, expected):
        """Test addition with different values."""
        assert a + b == expected
    
    @pytest.mark.parametrize("value", [
        0, 1, 2, 10, 100
    ])
    def test_positive_values(self, value):
        """Test that values are positive or zero."""
        assert value >= 0
    
    @pytest.mark.parametrize("value,square", [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
    ])
    def test_square_function(self, value, square):
        """Test the square function with different values."""
        assert value ** 2 == square
        
    # Example with multiple parametrize decorators (they work as a product)
    @pytest.mark.parametrize("x", [0, 1])
    @pytest.mark.parametrize("y", [2, 3])
    def test_multiple_parametrize(self, x, y):
        """Test with multiple parametrize decorators."""
        # This will run with (x,y) values: (0,2), (0,3), (1,2), (1,3)
        assert x < y 