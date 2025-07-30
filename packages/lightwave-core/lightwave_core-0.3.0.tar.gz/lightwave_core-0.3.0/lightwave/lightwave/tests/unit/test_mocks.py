"""Tests for mock objects used in testing."""

import pytest

from lightwave_ai.core.ai.base import LLMProvider, LLMRequest, LLMResponse


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""
    
    def __init__(self, model="mock-model", responses=None):
        """Initialize the mock provider.
        
        Args:
            model: Model name
            responses: Predefined responses to return for requests
        """
        super().__init__()
        self.model = model
        self.responses = responses or {}
        self.requests = []
        
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response for the request.
        
        Args:
            request: Request to generate a response for
            
        Returns:
            Response from the provider
        """
        self.requests.append(request)
        
        # Use pre-defined response if available
        if request.prompt in self.responses:
            return self.responses[request.prompt]
        
        # Return a default response
        return LLMResponse(
            text=f"This is a mock response for: {request.prompt}",
            model=self.model,
            usage={
                "prompt_tokens": len(request.prompt.split()),
                "completion_tokens": 10,
                "total_tokens": len(request.prompt.split()) + 10
            },
            raw_response={"mock": True}
        )


@pytest.mark.unit
class TestMockLLMProvider:
    """Tests for the MockLLMProvider class."""
    
    @pytest.fixture
    def provider(self):
        """Create a mock provider."""
        return MockLLMProvider()
    
    @pytest.fixture
    def provider_with_responses(self):
        """Create a mock provider with pre-defined responses."""
        responses = {
            "Hello": LLMResponse(
                text="World",
                model="mock-model",
                usage={"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
                raw_response={"mock": True}
            )
        }
        return MockLLMProvider(responses=responses)
    
    @pytest.mark.asyncio
    async def test_generate_default(self, provider):
        """Test generating a response with default behavior."""
        request = LLMRequest(prompt="Test prompt")
        response = await provider.generate(request)
        
        assert "This is a mock response for: Test prompt" == response.text
        assert provider.model == response.model
        assert 1 == len(provider.requests)
        assert request == provider.requests[0]
    
    @pytest.mark.asyncio
    async def test_generate_predefined(self, provider_with_responses):
        """Test generating a response with a pre-defined response."""
        request = LLMRequest(prompt="Hello")
        response = await provider_with_responses.generate(request)
        
        assert "World" == response.text
        assert 1 == len(provider_with_responses.requests) 