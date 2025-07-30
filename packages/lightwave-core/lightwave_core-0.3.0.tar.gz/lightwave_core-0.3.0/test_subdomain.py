"""Tests for the subdomain utilities module."""

import os
import pytest
from unittest.mock import patch, mock_open, MagicMock

from lightwave.core.utils.subdomain import (
    load_config,
    get_application_name,
    get_host_url,
    get_subdomain_list,
    is_subdomain_enabled,
    get_parent_domain,
    get_full_domain,
    get_current_subdomain
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

class TestSubdomainUtils:
    """Tests for the subdomain utility functions."""

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

    @patch('django.conf.settings')
    def test_get_application_name_from_settings(self, mock_settings):
        """Test getting application name from Django settings."""
        # Configure mock to have LIGHTWAVE_APPLICATION attribute
        mock_settings.LIGHTWAVE_APPLICATION = 'cineos'
        
        app_name = get_application_name()
        assert app_name == 'cineos'

    @patch('django.conf.settings', spec={})
    @patch('os.environ.get')
    def test_get_application_name_from_env(self, mock_env_get, mock_settings):
        """Test getting application name from environment variable."""
        # Configure mock to return application name
        mock_env_get.return_value = 'photographyos'
        
        app_name = get_application_name()
        assert app_name == 'photographyos'
        mock_env_get.assert_called_once_with('LIGHTWAVE_APPLICATION', 'createos')

    @patch('django.conf.settings', spec={})
    @patch('os.environ.get')
    def test_get_application_name_default(self, mock_env_get, mock_settings):
        """Test getting default application name."""
        # Configure env mock to return None (no env var set)
        mock_env_get.return_value = None
        
        app_name = get_application_name()
        assert app_name == 'createos'  # Default value
        mock_env_get.assert_called_once_with('LIGHTWAVE_APPLICATION', 'createos')

    @patch('lightwave.core.utils.subdomain.config', {
        'applications': {
            'createos': {
                'enabled_subdomains': ['admin', 'api', 'app'],
                'default_host': 'app',
                'parent_host': 'createos.io'
            }
        },
        'common_subdomains': {
            'admin': {'host_conf_name': 'admin_host'},
            'api': {'host_conf_name': 'api_host'},
            'app': {'host_conf_name': 'app_host'}
        }
    })
    @patch('lightwave.core.utils.subdomain.get_application_name')
    @patch('django_hosts.resolvers.reverse')
    def test_get_host_url(self, mock_reverse, mock_get_app):
        """Test generating a URL for a specific subdomain and view."""
        # Configure mocks
        mock_get_app.return_value = 'createos'
        mock_reverse.return_value = 'https://api.example.com/endpoint'
        
        # Call the function
        url = get_host_url('endpoint', 'api', scheme='https')
        
        # Verify the result
        assert url == 'https://api.example.com/endpoint'
        mock_reverse.assert_called_once_with('endpoint', host='api_host', 
                                            kwargs=None, scheme='https', 
                                            current_app=None)

    @patch('lightwave.core.utils.subdomain.config', {
        'applications': {
            'createos': {
                'enabled_subdomains': ['admin', 'api', 'app'],
                'default_host': 'app',
                'parent_host': 'createos.io'
            }
        },
        'common_subdomains': {
            'admin': {'host_conf_name': 'admin_host'},
            'api': {'host_conf_name': 'api_host'},
            'app': {'host_conf_name': 'app_host'}
        }
    })
    @patch('lightwave.core.utils.subdomain.get_application_name')
    def test_get_subdomain_list(self, mock_get_app):
        """Test getting the list of enabled subdomains."""
        # Configure mock
        mock_get_app.return_value = 'createos'
        
        # Call the function
        subdomains = get_subdomain_list()
        
        # Verify the result
        assert subdomains == ['admin', 'api', 'app']

    @patch('lightwave.core.utils.subdomain.get_subdomain_list')
    def test_is_subdomain_enabled_true(self, mock_get_list):
        """Test checking if a subdomain is enabled (true case)."""
        # Configure mock
        mock_get_list.return_value = ['admin', 'api', 'app']
        
        # Call the function
        result = is_subdomain_enabled('api')
        
        # Verify the result
        assert result is True

    @patch('lightwave.core.utils.subdomain.get_subdomain_list')
    def test_is_subdomain_enabled_false(self, mock_get_list):
        """Test checking if a subdomain is enabled (false case)."""
        # Configure mock
        mock_get_list.return_value = ['admin', 'api', 'app']
        
        # Call the function
        result = is_subdomain_enabled('shop')
        
        # Verify the result
        assert result is False

    @patch('lightwave.core.utils.subdomain.config', {
        'applications': {
            'createos': {
                'enabled_subdomains': ['admin', 'api', 'app'],
                'default_host': 'app',
                'parent_host': 'createos.io'
            }
        }
    })
    @patch('lightwave.core.utils.subdomain.get_application_name')
    def test_get_parent_domain(self, mock_get_app):
        """Test getting the parent domain for the current application."""
        # Configure mock
        mock_get_app.return_value = 'createos'
        
        # Call the function
        domain = get_parent_domain()
        
        # Verify the result
        assert domain == 'createos.io'

    @patch('lightwave.core.utils.subdomain.get_parent_domain')
    def test_get_full_domain_with_subdomain(self, mock_get_parent):
        """Test getting full domain with subdomain."""
        # Configure mock
        mock_get_parent.return_value = 'example.com'
        
        # Call the function
        domain = get_full_domain('api')
        
        # Verify the result
        assert domain == 'api.example.com'

    @patch('lightwave.core.utils.subdomain.get_parent_domain')
    def test_get_full_domain_without_subdomain(self, mock_get_parent):
        """Test getting full domain without subdomain."""
        # Configure mock
        mock_get_parent.return_value = 'example.com'
        
        # Call the function
        domain = get_full_domain()
        
        # Verify the result
        assert domain == 'example.com'

    @patch('lightwave.core.utils.subdomain.get_parent_domain')
    def test_get_current_subdomain(self, mock_get_parent):
        """Test getting current subdomain from request."""
        # Configure mock
        mock_get_parent.return_value = 'example.com'
        
        # Create a mock request
        request = MagicMock()
        request.get_host.return_value = 'api.example.com'
        
        # Call the function
        subdomain = get_current_subdomain(request)
        
        # Verify the result
        assert subdomain == 'api'

    @patch('lightwave.core.utils.subdomain.get_parent_domain')
    def test_get_current_subdomain_no_subdomain(self, mock_get_parent):
        """Test getting current subdomain with no subdomain in request."""
        # Configure mock
        mock_get_parent.return_value = 'example.com'
        
        # Create a mock request
        request = MagicMock()
        request.get_host.return_value = 'example.com'
        
        # Call the function
        subdomain = get_current_subdomain(request)
        
        # Verify the result
        assert subdomain is None

    def test_get_current_subdomain_invalid_request(self):
        """Test getting current subdomain with invalid request."""
        # Create an object that doesn't have get_host method
        request = object()
        
        # Call the function
        subdomain = get_current_subdomain(request)
        
        # Verify the result
        assert subdomain is None 