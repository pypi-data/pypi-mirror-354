"""
Enterprise Configuration Management System.

This module provides a comprehensive configuration management system
following enterprise patterns from Google, Microsoft, and Netflix.
Supports multiple configuration sources, environment-specific settings,
validation, and secure secret management.

Key Features:
- Multi-source configuration loading (files, environment, defaults)
- Pydantic-based validation and type safety
- Environment-specific configuration profiles
- Security-first approach with secret management
- Database connection management (SQLModel + Django compatibility)
- Structured logging configuration
- API and service configuration standards

Usage:
    Basic usage:
        from lightwave.core.config import get_config, load_config
        
        # Load from file
        config = load_config("config.yaml")
        
        # Get current config (loads defaults if none set)
        config = get_config()
        
        # Access config sections
        db_url = config.database.url
        api_port = config.api.port
        log_level = config.logging.level
    
    Advanced usage:
        from lightwave.core.config import ConfigManager, ConfigLoader
        
        # Manual configuration management
        manager = ConfigManager()
        manager.load_from_file("production.yaml")
        config = manager.get_config()
        
        # Custom loader with environment overrides
        loader = ConfigLoader()
        config = loader.load_from_file("base.yaml", allow_env_override=True)

Environment Variables:
    Configuration can be overridden with environment variables using
    the LIGHTWAVE_ prefix. Examples:
    
    - LIGHTWAVE_SERVICE_NAME: Override service name
    - LIGHTWAVE_ENVIRONMENT: Set environment (development/staging/production)
    - LIGHTWAVE_DATABASE_URL: Override database URL
    - LIGHTWAVE_API_PORT: Override API port
    - LIGHTWAVE_LOGGING_LEVEL: Override log level
    - LIGHTWAVE_SECRET_KEY: Override security secret key

Examples:
    Django integration:
        from lightwave.core.config import get_config
        
        config = get_config()
        
        # Use in Django settings
        DEBUG = config.api.debug
        SECRET_KEY = config.security.secret_key
        DATABASES = {"default": config.database.to_django_config()}
    
    FastAPI integration:
        from lightwave.core.config import get_config
        from fastapi import FastAPI
        
        config = get_config()
        
        app = FastAPI(
            title=config.service_name,
            version=config.version,
            debug=config.api.debug
        )
    
    SQLModel integration:
        from lightwave.core.config import get_config
        from sqlmodel import create_engine
        
        config = get_config()
        engine = create_engine(
            config.database.to_sqlalchemy_url(),
            pool_size=config.database.pool_size,
            max_overflow=config.database.max_overflow,
            echo=config.database.echo
        )
"""

from .models import (
    # Core configuration models
    DatabaseConfig,
    ApiConfig,
    LoggingConfig,
    SecurityConfig,
    LightwaveConfig,
    
    # Enums and constants
    Environment,
    LogLevel,
    
    # Exceptions
    ConfigValidationError,
    ConfigLoadError,
)

from .loader import (
    ConfigLoader,
    ConfigManager,
)

from .utils import (
    # Convenience functions
    load_config,
    get_config,
    set_config_path,
    reload_config,
    
    # Environment detection
    detect_environment,
    is_development,
    is_staging,
    is_production,
    
    # Validation utilities
    validate_config_file,
    validate_environment_vars,
)

# Version information
__version__ = "1.0.0"
__author__ = "Joel Schaeffer"

# Default configuration paths to search
DEFAULT_CONFIG_PATHS = [
    "lightwave.yaml",
    "lightwave.yml", 
    "config/lightwave.yaml",
    "config/lightwave.yml",
    "lightwave.json",
    "config/lightwave.json",
    ".lightwave/config.yaml",
    ".lightwave/config.yml",
]

# Environment variable prefix
ENV_PREFIX = "LIGHTWAVE_"

# Export all public symbols
__all__ = [
    # Models
    "DatabaseConfig",
    "ApiConfig", 
    "LoggingConfig",
    "SecurityConfig",
    "LightwaveConfig",
    
    # Enums
    "Environment",
    "LogLevel",
    
    # Exceptions
    "ConfigValidationError",
    "ConfigLoadError",
    
    # Loaders
    "ConfigLoader",
    "ConfigManager",
    
    # Convenience functions
    "load_config",
    "get_config", 
    "set_config_path",
    "reload_config",
    
    # Environment utilities
    "detect_environment",
    "is_development",
    "is_staging", 
    "is_production",
    
    # Validation
    "validate_config_file",
    "validate_environment_vars",
    
    # Constants
    "DEFAULT_CONFIG_PATHS",
    "ENV_PREFIX",
]