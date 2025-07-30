"""Tests for core agent functionality."""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from lightwave_ai.agents.base import BaseAgent
from lightwave_ai.config import Settings

@pytest.mark.unit
class TestCoreAgents:
    """Test suite for core agent functionality."""
    
    @pytest.fixture
    def test_settings(self) -> Settings:
        """Create test settings."""
        return Settings(
            ENV="testing",
            DEBUG=True,
            API_KEY="test-api-key",
            OPENAI_API_KEY="test-openai-key",
            ANTHROPIC_API_KEY="test-anthropic-key"
        )
    
    @pytest.fixture
    def mock_llm_provider(self):
        """Create a mock LLM provider."""
        provider = Mock()
        provider.generate.return_value = "Test response"
        return provider
    
    def test_agent_initialization(self, test_settings: Settings):
        """Test basic agent initialization."""
        agent = BaseAgent(settings=test_settings)
        
        assert agent.settings.ENV == "testing"
        assert agent.settings.DEBUG is True
        assert agent.settings.API_KEY == "test-api-key"
    
    def test_agent_with_custom_config(self, test_settings: Settings):
        """Test agent initialization with custom configuration."""
        custom_config = {
            "model": "test-model",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        agent = BaseAgent(settings=test_settings, **custom_config)
        
        assert agent.model == "test-model"
        assert agent.temperature == 0.7
        assert agent.max_tokens == 1000
    
    @patch("lightwave_ai.agents.base.get_llm_provider")
    def test_agent_llm_integration(self, mock_get_provider, test_settings: Settings, mock_llm_provider):
        """Test agent integration with LLM provider."""
        mock_get_provider.return_value = mock_llm_provider
        
        agent = BaseAgent(settings=test_settings)
        response = agent.generate("Test prompt")
        
        assert response == "Test response"
        mock_llm_provider.generate.assert_called_once_with("Test prompt")
    
    def test_agent_error_handling(self, test_settings: Settings):
        """Test agent error handling."""
        agent = BaseAgent(settings=test_settings)
        
        # Test with invalid settings
        with pytest.raises(ValueError):
            agent.validate_settings(Settings(ENV="invalid"))
        
        # Test with invalid model configuration
        with pytest.raises(ValueError):
            agent.validate_config({"temperature": 2.0})  # Temperature should be between 0 and 1
    
    @pytest.mark.asyncio
    async def test_agent_async_operations(self, test_settings: Settings, mock_llm_provider):
        """Test agent async operations."""
        agent = BaseAgent(settings=test_settings)
        agent._llm_provider = mock_llm_provider  # Inject mock provider
        
        mock_llm_provider.agenerate = Mock()
        mock_llm_provider.agenerate.return_value = "Async test response"
        
        response = await agent.agenerate("Test prompt")
        
        assert response == "Async test response"
        mock_llm_provider.agenerate.assert_called_once_with("Test prompt")
    
    def test_agent_context_management(self, test_settings: Settings):
        """Test agent context management."""
        agent = BaseAgent(settings=test_settings)
        
        # Test context initialization
        assert agent.context == {}
        
        # Test context update
        test_context = {"key": "value"}
        agent.update_context(test_context)
        assert agent.context == test_context
        
        # Test context clear
        agent.clear_context()
        assert agent.context == {}
    
    def test_agent_configuration_validation(self, test_settings: Settings):
        """Test agent configuration validation."""
        # Test valid configuration
        valid_config = {
            "model": "test-model",
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 0.9
        }
        
        agent = BaseAgent(settings=test_settings, **valid_config)
        assert agent.validate_config(valid_config) is None
        
        # Test invalid configurations
        invalid_configs = [
            {"temperature": -0.1},  # Temperature too low
            {"temperature": 1.1},   # Temperature too high
            {"max_tokens": 0},      # Invalid token count
            {"top_p": 1.5}         # Invalid top_p value
        ]
        
        for config in invalid_configs:
            with pytest.raises(ValueError):
                agent.validate_config(config)
    
    def test_agent_state_management(self, test_settings: Settings):
        """Test agent state management."""
        agent = BaseAgent(settings=test_settings)
        
        # Test initial state
        assert agent.is_initialized
        assert not agent.is_busy
        
        # Test state transitions
        agent.start_processing()
        assert agent.is_busy
        
        agent.end_processing()
        assert not agent.is_busy
        
        # Test state validation
        with pytest.raises(RuntimeError):
            agent.start_processing()  # Can't start when already busy
            agent.generate("Test prompt")  # Can't generate when busy 