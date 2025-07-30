"""
Configuration Utilities and Convenience Functions.

Provides high-level functions for common configuration operations,
environment detection, and validation utilities.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

from .models import LightwaveConfig, Environment, ConfigValidationError, ConfigLoadError
from .loader import _config_manager


def load_config(
    file_path: Union[str, Path], 
    allow_env_override: bool = True
) -> LightwaveConfig:
    """
    Load configuration from file.
    
    Args:
        file_path: Path to configuration file (YAML or JSON)
        allow_env_override: Whether to allow environment variable overrides
    
    Returns:
        Loaded and validated configuration
    
    Raises:
        ConfigLoadError: If file cannot be loaded
        ConfigValidationError: If configuration is invalid
    
    Example:
        config = load_config("config.yaml")
        print(f"Service: {config.service_name}")
        print(f"Database: {config.database.url}")
    """
    return _config_manager.load_from_file(file_path, allow_env_override)


def get_config() -> LightwaveConfig:
    """
    Get current configuration.
    
    If no configuration is loaded, attempts to auto-load from common paths
    or falls back to defaults.
    
    Returns:
        Current configuration instance
    
    Example:
        config = get_config()
        if config.environment.is_production:
            print("Running in production mode")
    """
    return _config_manager.get_config()


def set_config_path(file_path: Union[str, Path]) -> LightwaveConfig:
    """
    Set configuration file path and load it.
    
    Args:
        file_path: Path to configuration file
    
    Returns:
        Loaded configuration
    
    Example:
        config = set_config_path("/etc/lightwave/config.yaml")
    """
    return _config_manager.load_from_file(file_path)


def reload_config() -> LightwaveConfig:
    """
    Reload configuration from the same source.
    
    Returns:
        Reloaded configuration
    
    Example:
        # After config file changes
        config = reload_config()
    """
    return _config_manager.reload()


def is_config_loaded() -> bool:
    """
    Check if configuration is loaded.
    
    Returns:
        True if configuration is loaded, False otherwise
    """
    return _config_manager.is_loaded()


def get_config_source() -> str:
    """
    Get description of current configuration source.
    
    Returns:
        String describing configuration source
    
    Example:
        source = get_config_source()
        print(f"Config loaded from: {source}")
    """
    return _config_manager.get_config_source()


# Environment Detection Functions
def detect_environment() -> Environment:
    """
    Detect current environment from various sources.
    
    Checks in order:
    1. LIGHTWAVE_ENVIRONMENT environment variable
    2. Environment-specific environment variables
    3. Default to development
    
    Returns:
        Detected environment
    
    Example:
        env = detect_environment()
        if env.is_production:
            setup_production_logging()
    """
    # Check explicit environment variable
    env_str = os.getenv("LIGHTWAVE_ENVIRONMENT", "").lower()
    if env_str:
        try:
            return Environment(env_str)
        except ValueError:
            pass
    
    # Check for environment-specific variables
    if os.getenv("PRODUCTION") or os.getenv("PROD"):
        return Environment.PRODUCTION
    
    if os.getenv("STAGING") or os.getenv("STAGE"):
        return Environment.STAGING
    
    if os.getenv("TESTING") or os.getenv("TEST"):
        return Environment.TESTING
    
    # Check for development indicators
    if os.getenv("DEBUG") or os.getenv("DEV") or os.getenv("DEVELOPMENT"):
        return Environment.DEVELOPMENT
    
    # Default to development
    return Environment.DEVELOPMENT


def is_development() -> bool:
    """Check if running in development environment."""
    return detect_environment() == Environment.DEVELOPMENT


def is_staging() -> bool:
    """Check if running in staging environment.""" 
    return detect_environment() == Environment.STAGING


def is_production() -> bool:
    """Check if running in production environment."""
    return detect_environment() == Environment.PRODUCTION


def is_testing() -> bool:
    """Check if running in testing environment."""
    return detect_environment() == Environment.TESTING


# Validation Utilities
def validate_config_file(file_path: Union[str, Path]) -> bool:
    """
    Validate configuration file without loading it.
    
    Args:
        file_path: Path to configuration file
    
    Returns:
        True if file is valid, False otherwise
    
    Example:
        if validate_config_file("config.yaml"):
            config = load_config("config.yaml")
        else:
            print("Invalid configuration file")
    """
    try:
        load_config(file_path)
        return True
    except (ConfigLoadError, ConfigValidationError):
        return False


def validate_environment_vars(env_prefix: str = "LIGHTWAVE_") -> List[str]:
    """
    Validate environment variables for configuration.
    
    Args:
        env_prefix: Environment variable prefix to check
    
    Returns:
        List of validation errors (empty if all valid)
    
    Example:
        errors = validate_environment_vars()
        if errors:
            for error in errors:
                print(f"Config error: {error}")
    """
    from .loader import ConfigLoader
    
    errors = []
    loader = ConfigLoader(env_prefix)
    
    try:
        config_dict = loader._extract_config_from_env()
        if config_dict:
            # Try to validate by creating a minimal config
            test_config = {
                "service_name": "validation-test",
                "version": "1.0.0",
                **config_dict
            }
            loader.load_from_dict(test_config)
    except ConfigValidationError as e:
        errors.append(str(e))
    except Exception as e:
        errors.append(f"Unexpected validation error: {e}")
    
    return errors


def get_database_url() -> str:
    """
    Get database URL from current configuration.
    
    Returns:
        Database connection URL
    
    Example:
        db_url = get_database_url()
        engine = create_engine(db_url)
    """
    config = get_config()
    return config.database.url


def get_api_base_url() -> str:
    """
    Get API base URL from current configuration.
    
    Returns:
        API base URL
    
    Example:
        base_url = get_api_base_url()
        client = ApiClient(base_url)
    """
    config = get_config()
    return config.api.base_url


def get_log_level() -> str:
    """
    Get logging level from current configuration.
    
    Returns:
        Log level string
    
    Example:
        log_level = get_log_level()
        logging.basicConfig(level=log_level)
    """
    config = get_config()
    return config.logging.level.value


def get_secret_key() -> str:
    """
    Get secret key from current configuration.
    
    Returns:
        Secret key for cryptographic operations
    
    Example:
        secret = get_secret_key()
        jwt_token = encode_jwt(payload, secret)
    """
    config = get_config()
    return config.security.secret_key


def is_debug_enabled() -> bool:
    """
    Check if debug mode is enabled.
    
    Returns:
        True if debug mode is enabled
    
    Example:
        if is_debug_enabled():
            print("Debug mode is active")
    """
    config = get_config()
    return config.api.debug


def get_cors_origins() -> List[str]:
    """
    Get CORS origins from current configuration.
    
    Returns:
        List of allowed CORS origins
    
    Example:
        origins = get_cors_origins()
        app.add_middleware(CORSMiddleware, allow_origins=origins)
    """
    config = get_config()
    return config.api.cors_origins


def get_feature_flag(feature_name: str, default: bool = False) -> bool:
    """
    Get feature flag value from current configuration.
    
    Args:
        feature_name: Name of the feature flag
        default: Default value if flag not found
    
    Returns:
        Feature flag value
    
    Example:
        if get_feature_flag("new_ui_enabled"):
            render_new_ui()
        else:
            render_old_ui()
    """
    config = get_config()
    return config.features.get(feature_name, default)


def get_integration_config(integration_name: str) -> Dict[str, Any]:
    """
    Get integration configuration.
    
    Args:
        integration_name: Name of the integration
    
    Returns:
        Integration configuration dictionary
    
    Example:
        redis_config = get_integration_config("redis")
        redis_client = Redis(**redis_config)
    """
    config = get_config()
    return config.integrations.get(integration_name, {})


def create_config_template(
    service_name: str,
    version: str = "1.0.0",
    environment: Environment = Environment.DEVELOPMENT,
    output_path: Optional[Union[str, Path]] = None
) -> str:
    """
    Create a configuration template file.
    
    Args:
        service_name: Name of the service
        version: Service version
        environment: Target environment
        output_path: Path to save template (None for string return)
    
    Returns:
        Configuration template as YAML string
    
    Example:
        template = create_config_template("my-service", "1.0.0")
        with open("config.yaml", "w") as f:
            f.write(template)
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required for template creation. Install with: pip install pyyaml")
    
    # Create a sample configuration
    config = LightwaveConfig(
        service_name=service_name,
        version=version,
        environment=environment,
        description=f"Configuration for {service_name}",
    )
    
    # Convert to dictionary and add comments structure
    config_dict = config.model_dump()
    
    template = f"""# Lightwave Configuration for {service_name}
# Generated configuration template

# Service Information
service_name: {config_dict['service_name']}
version: {config_dict['version']}
environment: {config_dict['environment']}
description: {config_dict.get('description', '')}

# Database Configuration
database:
  url: {config_dict['database']['url']}
  pool_size: {config_dict['database']['pool_size']}
  max_overflow: {config_dict['database']['max_overflow']}
  echo: {str(config_dict['database']['echo']).lower()}

# API Configuration  
api:
  host: {config_dict['api']['host']}
  port: {config_dict['api']['port']}
  debug: {str(config_dict['api']['debug']).lower()}
  cors_origins: []
  
# Logging Configuration
logging:
  level: {config_dict['logging']['level']}
  format: "{config_dict['logging']['format']}"
  file_path: null  # Set to file path for file logging
  
# Security Configuration
security:
  secret_key: {config_dict['security']['secret_key']}
  jwt_expiration_hours: {config_dict['security']['jwt_expiration_hours']}
  allowed_hosts: []

# Feature Flags
features: {{}}

# Third-party Integrations
integrations: {{}}

# Custom Settings
custom: {{}}
"""
    
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(template)
    
    return template