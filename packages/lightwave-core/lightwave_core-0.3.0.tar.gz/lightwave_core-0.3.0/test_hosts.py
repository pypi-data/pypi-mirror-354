"""Tests for the hosts module."""

import os
import sys
import pytest
from unittest.mock import patch, mock_open, MagicMock

from lightwave.core.hosts import (
    load_config, 
    get_current_application, 
    get_application_config,
    get_host_patterns
)

# Sample YAML config for testing
SAMPLE_CONFIG = """
domains:
  createos:
    primary: createos.io
    description: Central business management platform
common_subdomains:
  admin:
    description: System administration and CMS
    required: true
    urls_module: admin_urls
    host_conf_name: admin_host
  api:
    description: API endpoints
    required: true
    urls_module: api_urls
    host_conf_name: api_host
applications:
  createos:
    enabled_subdomains:
      - admin
      - api
      - app
    default_host: app
    parent_host: createos.io
"""

class TestHostsModule:
    """Tests for the hosts.py module used for Django subdomains."""

    @patch('builtins.open', new_callable=mock_open, read_data=SAMPLE_CONFIG)
    def test_load_config(self, mock_file):
        """Test loading configuration from YAML file."""
        config = load_config()
        
        # Check if the file was opened
        mock_file.assert_called_once()
        
        # Verify the config is loaded correctly
        assert 'domains' in config
        assert 'createos' in config['domains']
        assert 'common_subdomains' in config
        assert 'admin' in config['common_subdomains']
        assert 'applications' in config
        assert 'createos' in config['applications']

    @patch('builtins.open', new_callable=mock_open, read_data='invalid: yaml: :')
    def test_load_config_invalid(self, mock_file):
        """Test loading invalid configuration raises exception."""
        with pytest.raises(RuntimeError):
            load_config()

    @patch('os.environ.get')
    @patch('django.conf.settings')
    def test_get_current_application_from_settings(self, mock_settings, mock_env_get):
        """Test getting application name from Django settings."""
        # Configure mock to have LIGHTWAVE_APPLICATION attribute
        mock_settings.LIGHTWAVE_APPLICATION = 'cineos'
        
        app_name = get_current_application()
        assert app_name == 'cineos'
        # The environment variable should not be checked
        mock_env_get.assert_not_called()

    @patch('os.environ.get')
    @patch('django.conf.settings', spec={})
    def test_get_current_application_from_env(self, mock_settings, mock_env_get):
        """Test getting application name from environment variable."""
        # Configure mock to return application name
        mock_env_get.return_value = 'photographyos'
        
        app_name = get_current_application()
        assert app_name == 'photographyos'
        mock_env_get.assert_called_once_with('LIGHTWAVE_APPLICATION', 'createos')

    @patch('os.environ.get')
    @patch('django.conf.settings', spec={})
    def test_get_current_application_default(self, mock_settings, mock_env_get):
        """Test getting default application name."""
        # Configure env mock to return None (no env var set)
        mock_env_get.return_value = None
        
        app_name = get_current_application()
        assert app_name == 'createos'  # Default value
        mock_env_get.assert_called_once_with('LIGHTWAVE_APPLICATION', 'createos')

    @patch('lightwave.core.hosts.load_config')
    @patch('lightwave.core.hosts.get_current_application')
    def test_get_application_config(self, mock_get_app, mock_load_config):
        """Test getting application configuration."""
        # Mock configuration and application name
        mock_load_config.return_value = {
            'applications': {
                'cineos': {'default_host': 'app', 'parent_host': 'cineos.io'}
            }
        }
        mock_get_app.return_value = 'cineos'
        
        app_config = get_application_config()
        assert app_config == {'default_host': 'app', 'parent_host': 'cineos.io'}

    @patch('lightwave.core.hosts.load_config')
    @patch('lightwave.core.hosts.get_current_application')
    def test_get_application_config_not_found(self, mock_get_app, mock_load_config):
        """Test getting non-existent application configuration raises exception."""
        # Mock configuration and non-existent application name
        mock_load_config.return_value = {'applications': {}}
        mock_get_app.return_value = 'non_existent_app'
        
        with pytest.raises(RuntimeError):
            get_application_config()

    @patch('lightwave.core.hosts.get_application_config')
    @patch('lightwave.core.hosts.get_current_application')
    @patch('lightwave.core.hosts.load_config')
    @patch('django.conf.settings')
    @patch('django_hosts.host')
    def test_get_host_patterns(self, mock_host, mock_settings, mock_load_config, 
                               mock_get_app, mock_get_app_config):
        """Test generating host patterns."""
        # Configure mocks
        mock_settings.ROOT_URLCONF = 'myproject.urls'
        mock_get_app.return_value = 'createos'
        mock_get_app_config.return_value = {
            'default_host': 'app',
            'enabled_subdomains': ['admin', 'api']
        }
        mock_load_config.return_value = {
            'common_subdomains': {
                'admin': {
                    'urls_module': 'admin_urls',
                    'host_conf_name': 'admin_host'
                },
                'api': {
                    'urls_module': 'api_urls',
                    'host_conf_name': 'api_host'
                }
            }
        }
        
        # Create return values for mock_host calls
        default_host_pattern = MagicMock()
        admin_host_pattern = MagicMock()
        api_host_pattern = MagicMock()
        
        # Configure mock_host to return different values depending on args
        mock_host.side_effect = [default_host_pattern, admin_host_pattern, api_host_pattern]
        
        # Call the function under test
        host_patterns = get_host_patterns()
        
        # Verify the result
        assert len(host_patterns) == 3
        assert default_host_pattern in host_patterns
        assert admin_host_pattern in host_patterns
        assert api_host_pattern in host_patterns
        
        # Verify mock_host was called correctly
        assert mock_host.call_count == 3 