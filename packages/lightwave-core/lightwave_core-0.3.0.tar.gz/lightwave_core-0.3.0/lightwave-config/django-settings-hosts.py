"""
Django Host Settings Integration Helper
This module provides utilities to integrate django-hosts into Django settings.
"""
import os
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def configure_hosts_settings(settings_module):
    """
    Configure django-hosts settings in the Django settings module.
    
    Args:
        settings_module: The Django settings module to configure.
    """
    # Load configuration
    config = load_host_config(settings_module)
    
    # Get django-hosts settings
    hosts_settings = config.get('django_hosts_settings', {})
    settings_dict = hosts_settings.get('settings', {})
    
    # Determine the application
    app_name = getattr(settings_module, 'LIGHTWAVE_APPLICATION', 'default')
    app_config = config.get('applications', {}).get(app_name, {})
    
    # Configure settings from config
    for key, value in settings_dict.items():
        setattr(settings_module, key, value)
    
    # Set environment-specific settings
    env = getattr(settings_module, 'ENVIRONMENT', 'development')
    env_config = config.get('environments', {}).get(env, {})
    
    # Override parent host if specified in environment
    if env_config.get('parent_host'):
        setattr(settings_module, 'PARENT_HOST', env_config['parent_host'])
    elif app_config.get('parent_host'):
        setattr(settings_module, 'PARENT_HOST', app_config['parent_host'])
    
    # Override default host if specified in environment
    if env_config.get('default_host'):
        setattr(settings_module, 'DEFAULT_HOST', env_config['default_host'])
    elif app_config.get('default_host'):
        setattr(settings_module, 'DEFAULT_HOST', app_config['default_host'])
    
    # Configure middleware
    middleware = getattr(settings_module, 'MIDDLEWARE', [])
    middleware_config = hosts_settings.get('middleware', {})
    middleware_positions = hosts_settings.get('middleware_position', {})
    
    # Add host request middleware
    req_middleware = middleware_config.get('host_middleware', 'django_hosts.middleware.HostsRequestMiddleware')
    req_pos = middleware_positions.get('host_middleware', 0)  # Default to first position
    if req_middleware not in middleware:
        middleware.insert(req_pos, req_middleware)
    
    # Add host response middleware
    res_middleware = middleware_config.get('host_response_middleware', 'django_hosts.middleware.HostsResponseMiddleware')
    res_pos = middleware_positions.get('host_response_middleware', -1)  # Default to last position
    if res_middleware not in middleware:
        if res_pos < 0:
            middleware.append(res_middleware)
        else:
            middleware.insert(res_pos, res_middleware)
    
    # Update middleware in settings
    setattr(settings_module, 'MIDDLEWARE', middleware)
    
    # Add django-hosts context processor if not already added
    templates = getattr(settings_module, 'TEMPLATES', [])
    if templates:
        for template in templates:
            if template.get('BACKEND') == 'django.template.backends.django.DjangoTemplates':
                options = template.get('OPTIONS', {})
                context_processors = options.get('context_processors', [])
                hosts_processor = 'django_hosts.context_processors.hosts'
                if hosts_processor not in context_processors:
                    context_processors.append(hosts_processor)
                options['context_processors'] = context_processors
                template['OPTIONS'] = options
        
        # Update templates in settings
        setattr(settings_module, 'TEMPLATES', templates)
    
    # Make sure django_hosts is in INSTALLED_APPS
    installed_apps = getattr(settings_module, 'INSTALLED_APPS', [])
    if 'django_hosts' not in installed_apps:
        installed_apps.append('django_hosts')
        setattr(settings_module, 'INSTALLED_APPS', installed_apps)

def load_host_config(settings_module):
    """
    Load host configuration from YAML file.
    
    Args:
        settings_module: The Django settings module to use for path resolution.
    
    Returns:
        dict: The host configuration.
    """
    # Determine base directory
    base_dir = getattr(settings_module, 'BASE_DIR', None)
    if base_dir is None:
        # Try to infer BASE_DIR if not set
        if hasattr(settings_module, '__file__'):
            base_dir = Path(settings_module.__file__).resolve().parent.parent
        else:
            base_dir = Path.cwd()
    
    # Look for config in several locations
    config_paths = [
        os.path.join(base_dir, 'lightwave-config', 'django-hosts-config.yaml'),
        os.path.join(base_dir, 'config', 'django-hosts-config.yaml'),
        os.path.join(base_dir, 'django-hosts-config.yaml'),
    ]
    
    # Try each path
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as file:
                    config = yaml.safe_load(file)
                    logger.info(f"Loaded host configuration from {config_path}")
                    return config
            except (yaml.YAMLError) as e:
                logger.error(f"Error parsing hosts configuration from {config_path}: {e}")
    
    # If no config found, return default configuration
    logger.warning("No host configuration found, using default settings")
    return default_host_config()

def default_host_config():
    """
    Provide default host configuration when no config file is found.
    
    Returns:
        dict: Default host configuration.
    """
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
        },
        'django_hosts_settings': {
            'settings': {
                'ROOT_HOSTCONF': 'config.hosts',
                'DEFAULT_HOST': 'www',
                'HOST_PORT': '8000',
                'PARENT_HOST': 'localhost:8000',
            },
            'middleware': {
                'host_middleware': 'django_hosts.middleware.HostsRequestMiddleware',
                'host_response_middleware': 'django_hosts.middleware.HostsResponseMiddleware',
            },
            'middleware_position': {
                'host_middleware': 0,
                'host_response_middleware': -1,
            }
        }
    } 