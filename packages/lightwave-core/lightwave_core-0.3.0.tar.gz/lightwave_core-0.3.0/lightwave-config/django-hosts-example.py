"""
Django Hosts configuration for Lightwave projects.
This file demonstrates how to set up django-hosts for multi-domain/subdomain routing.
"""
from django.conf import settings
from django_hosts import patterns, host
import yaml
import os
import logging

logger = logging.getLogger(__name__)

def load_host_config():
    """
    Load host configuration from YAML file.
    Returns a dict with the host configuration.
    """
    config_path = os.path.join(settings.BASE_DIR, 'lightwave-config', 'django-hosts-config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.error(f"Error loading hosts configuration: {e}")
        # Return default configuration as fallback
        return {
            'environments': {
                'development': {
                    'default_host': 'www',
                    'parent_host': 'localhost:8000',
                    'hosts': [
                        {'name': 'www', 'app_name': 'www', 'subdomain': '', 'urlconf': 'website.urls'},
                        {'name': 'api', 'app_name': 'api', 'subdomain': 'api', 'urlconf': 'api.urls'},
                    ]
                }
            }
        }

def get_current_environment():
    """
    Determine the current environment based on settings.
    Returns the environment name (development, staging, production).
    """
    env = getattr(settings, 'ENVIRONMENT', 'development')
    return env

def get_host_callback(callback_name=None):
    """
    Get the host callback function from the configuration.
    If callback_name is None, returns the default callback.
    """
    config = load_host_config()
    
    # Get default callback from global settings
    default_callback = config.get('global_settings', {}).get(
        'host_callback', 'django_hosts.callbacks.cached_host_site'
    )
    
    if callback_name is None:
        return default_callback
    
    # Get custom callback if specified
    custom_callbacks = config.get('callbacks', {})
    if callback_name in custom_callbacks:
        callback_info = custom_callbacks[callback_name]
        return f"{callback_info['module']}.{callback_info['function']}"
    
    return default_callback

def get_hosts_for_environment(environment=None):
    """
    Get the hosts configuration for the specified environment.
    If environment is None, uses the current environment.
    Returns a list of host configurations.
    """
    if environment is None:
        environment = get_current_environment()
    
    config = load_host_config()
    env_config = config.get('environments', {}).get(environment, {})
    
    # Set parent host in settings if not already set
    if not hasattr(settings, 'PARENT_HOST') or not settings.PARENT_HOST:
        parent_host = env_config.get('parent_host', '')
        setattr(settings, 'PARENT_HOST', parent_host)
    
    # Set default host in settings if not already set
    if not hasattr(settings, 'DEFAULT_HOST') or not settings.DEFAULT_HOST:
        default_host = env_config.get('default_host', 'www')
        setattr(settings, 'DEFAULT_HOST', default_host)
    
    return env_config.get('hosts', [])

# Get host configurations for the current environment
host_list = get_hosts_for_environment()

# Define host patterns dynamically based on configuration
host_patterns = []
for host_config in host_list:
    name = host_config.get('name')
    app_name = host_config.get('app_name', name)
    subdomain = host_config.get('subdomain', '')
    urlconf = host_config.get('urlconf')
    callback_name = host_config.get('callback')
    
    # Get callback function
    callback = get_host_callback(callback_name)
    
    # Create host pattern
    host_patterns.append(
        host(subdomain, urlconf, name=app_name, callback=callback)
    )

# Create the host patterns that django-hosts will use
host_patterns = patterns('', *host_patterns) 