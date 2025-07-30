"""Host configuration and management for the Lightwave ecosystem."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class HostConfig:
    """Configuration for a host pattern."""
    name: str
    pattern: str
    scheme: str = "https"
    port: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None


def load_config(config_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to config file. If None, looks for default locations.
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file is not found
        yaml.YAMLError: If config file is invalid YAML
    """
    if config_path is None:
        # Default config locations
        possible_paths = [
            Path("lightwave-config.yaml"),
            Path("config/lightwave.yaml"),
            Path(".lightwave/config.yaml"),
            Path(os.path.expanduser("~/.lightwave/config.yaml"))
        ]
        
        config_path = None
        for path in possible_paths:
            if path.exists():
                config_path = path
                break
        
        if config_path is None:
            raise FileNotFoundError("No configuration file found in default locations")
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return config or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in config file {config_path}: {e}")


def get_current_application() -> str:
    """Get the current application name from environment or config.
    
    Returns:
        Application name
    """
    # Check environment variable first
    app_name = os.environ.get('LIGHTWAVE_APPLICATION')
    if app_name:
        return app_name
    
    # Try to get from config
    try:
        config = load_config()
        return config.get('application', 'default')
    except FileNotFoundError:
        return 'default'


def get_application_config(app_name: Optional[str] = None) -> Dict[str, Any]:
    """Get configuration for a specific application.
    
    Args:
        app_name: Application name. If None, uses current application.
        
    Returns:
        Application configuration dictionary
    """
    if app_name is None:
        app_name = get_current_application()
    
    try:
        config = load_config()
        applications = config.get('applications', {})
        return applications.get(app_name, {})
    except FileNotFoundError:
        return {}


def get_host_patterns(app_name: Optional[str] = None) -> List[HostConfig]:
    """Get host patterns for an application.
    
    Args:
        app_name: Application name. If None, uses current application.
        
    Returns:
        List of HostConfig objects
    """
    app_config = get_application_config(app_name)
    hosts = app_config.get('hosts', [])
    
    host_configs = []
    for host_data in hosts:
        if isinstance(host_data, dict):
            host_config = HostConfig(
                name=host_data.get('name', 'default'),
                pattern=host_data.get('pattern', '*'),
                scheme=host_data.get('scheme', 'https'),
                port=host_data.get('port'),
                settings=host_data.get('settings', {})
            )
            host_configs.append(host_config)
    
    return host_configs


def match_host(hostname: str, pattern: str) -> bool:
    """Check if hostname matches a host pattern.
    
    Args:
        hostname: Hostname to check
        pattern: Pattern to match against (supports wildcards)
        
    Returns:
        True if hostname matches pattern
        
    Examples:
        >>> match_host("api.example.com", "*.example.com")
        True
        >>> match_host("example.com", "example.com")
        True
    """
    if pattern == '*':
        return True
    
    if '*' not in pattern:
        return hostname == pattern
    
    # Convert pattern to regex
    import re
    regex_pattern = pattern.replace('.', r'\.').replace('*', r'[^.]*')
    regex_pattern = f'^{regex_pattern}$'
    
    return bool(re.match(regex_pattern, hostname))


def get_host_for_request(hostname: str, app_name: Optional[str] = None) -> Optional[HostConfig]:
    """Get the host configuration that matches a request hostname.
    
    Args:
        hostname: Request hostname
        app_name: Application name. If None, uses current application.
        
    Returns:
        Matching HostConfig or None if no match found
    """
    host_patterns = get_host_patterns(app_name)
    
    for host_config in host_patterns:
        if match_host(hostname, host_config.pattern):
            return host_config
    
    return None


def validate_config(config_path: Optional[Union[str, Path]] = None) -> List[str]:
    """Validate configuration file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        return [str(e)]
    except yaml.YAMLError as e:
        return [str(e)]
    
    # Validate structure
    if not isinstance(config, dict):
        errors.append("Config must be a dictionary")
        return errors
    
    # Validate applications
    applications = config.get('applications', {})
    if not isinstance(applications, dict):
        errors.append("'applications' must be a dictionary")
    else:
        for app_name, app_config in applications.items():
            if not isinstance(app_config, dict):
                errors.append(f"Application '{app_name}' config must be a dictionary")
                continue
            
            # Validate hosts
            hosts = app_config.get('hosts', [])
            if not isinstance(hosts, list):
                errors.append(f"Application '{app_name}' hosts must be a list")
                continue
            
            for i, host in enumerate(hosts):
                if not isinstance(host, dict):
                    errors.append(f"Application '{app_name}' host {i} must be a dictionary")
                    continue
                
                if 'pattern' not in host:
                    errors.append(f"Application '{app_name}' host {i} missing 'pattern'")
                
                if 'name' not in host:
                    errors.append(f"Application '{app_name}' host {i} missing 'name'")
    
    return errors