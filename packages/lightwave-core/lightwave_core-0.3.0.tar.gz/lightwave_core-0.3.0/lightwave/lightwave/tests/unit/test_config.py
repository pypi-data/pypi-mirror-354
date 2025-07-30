"""Tests for the config module."""

import os
from unittest.mock import patch

import pytest

from lightwave_ai.config import Settings


@pytest.mark.unit
class TestSettings:
    """Tests for the Settings class."""
    
    def test_settings_defaults(self):
        """Test that default settings are loaded correctly."""
        settings = Settings()
        assert settings.ENV == "development"
        assert settings.DEBUG is True
        
    @patch.dict(os.environ, {"ENV": "production", "DEBUG": "false"})
    def test_settings_from_env(self):
        """Test that settings are loaded from environment variables."""
        settings = Settings()
        assert settings.ENV == "production"
        assert settings.DEBUG is False
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_provider_api_keys(self):
        """Test that provider API keys are loaded correctly."""
        settings = Settings()
        assert settings.OPENAI_API_KEY == "test-key"
    
    def test_log_level_default(self):
        """Test that log level defaults to INFO."""
        settings = Settings()
        assert settings.LOG_LEVEL == "INFO"
    
    @patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"})
    def test_log_level_from_env(self):
        """Test that log level is loaded from environment."""
        settings = Settings()
        assert settings.LOG_LEVEL == "DEBUG" 