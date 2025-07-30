"""
Configuration Loading and Management.

Enterprise-grade configuration loading system supporting multiple sources,
environment variable overrides, and validation. Follows the 12-factor app
methodology for configuration management.
"""

import os
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None
from typing import Dict, Any, Optional, Union, List
from threading import Lock

from .models import (
    LightwaveConfig,
    DatabaseConfig,
    ApiConfig,
    LoggingConfig,
    SecurityConfig,
    Environment,
    ConfigValidationError,
    ConfigLoadError
)


class ConfigLoader:
    """Loads configuration from various sources with validation."""
    
    def __init__(self, env_prefix: str = "LIGHTWAVE_"):
        """Initialize config loader with environment variable prefix."""
        self.env_prefix = env_prefix
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> LightwaveConfig:
        """Load configuration from dictionary."""
        try:
            return LightwaveConfig(**config_dict)
        except Exception as e:
            raise ConfigValidationError(f"Invalid configuration: {e}")
    
    def load_from_file(
        self, 
        file_path: Union[str, Path], 
        allow_env_override: bool = True
    ) -> LightwaveConfig:
        """Load configuration from YAML or JSON file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ConfigLoadError(f"Configuration file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() in ('.yaml', '.yml'):
                    if yaml is None:
                        raise ConfigLoadError("PyYAML is required for YAML configuration files. Install with: pip install pyyaml")
                    config_dict = yaml.safe_load(f)
                elif file_path.suffix.lower() == '.json':
                    config_dict = json.load(f)
                else:
                    raise ConfigLoadError(
                        f"Unsupported file format: {file_path.suffix}. "
                        "Use .yaml, .yml, or .json"
                    )
        except Exception as e:
            if yaml and hasattr(e, '__class__') and 'yaml' in e.__class__.__module__.lower():
                raise ConfigLoadError(f"Invalid YAML in {file_path}: {e}")
            elif isinstance(e, json.JSONDecodeError):
                raise ConfigLoadError(f"Invalid JSON in {file_path}: {e}")
            else:
                raise ConfigLoadError(f"Error reading {file_path}: {e}")
        
        if config_dict is None:
            config_dict = {}
        
        # Apply environment variable overrides
        if allow_env_override:
            config_dict = self._apply_env_overrides(config_dict)
        
        return self.load_from_dict(config_dict)
    
    def load_from_environment(self) -> LightwaveConfig:
        """Load configuration entirely from environment variables."""
        config_dict = self._extract_config_from_env()
        return self.load_from_dict(config_dict)
    
    def _apply_env_overrides(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to config dictionary."""
        env_config = self._extract_config_from_env()
        
        # Deep merge environment config into file config
        return self._deep_merge(config_dict, env_config)
    
    def _extract_config_from_env(self) -> Dict[str, Any]:
        """Extract configuration from environment variables."""
        config = {}
        
        # Service-level configuration
        if service_name := os.getenv(f"{self.env_prefix}SERVICE_NAME"):
            config["service_name"] = service_name
        
        if version := os.getenv(f"{self.env_prefix}VERSION"):
            config["version"] = version
        
        if environment := os.getenv(f"{self.env_prefix}ENVIRONMENT"):
            config["environment"] = environment
        
        if description := os.getenv(f"{self.env_prefix}DESCRIPTION"):
            config["description"] = description
        
        # Database configuration
        database_config = {}
        if db_url := os.getenv(f"{self.env_prefix}DATABASE_URL"):
            database_config["url"] = db_url
        
        if db_driver := os.getenv(f"{self.env_prefix}DATABASE_DRIVER"):
            database_config["driver"] = db_driver
        
        if db_pool_size := os.getenv(f"{self.env_prefix}DATABASE_POOL_SIZE"):
            try:
                database_config["pool_size"] = int(db_pool_size)
            except ValueError:
                pass
        
        if db_max_overflow := os.getenv(f"{self.env_prefix}DATABASE_MAX_OVERFLOW"):
            try:
                database_config["max_overflow"] = int(db_max_overflow)
            except ValueError:
                pass
        
        if db_echo := os.getenv(f"{self.env_prefix}DATABASE_ECHO"):
            database_config["echo"] = db_echo.lower() in ("true", "1", "yes", "on")
        
        if database_config:
            config["database"] = database_config
        
        # API configuration
        api_config = {}
        if api_host := os.getenv(f"{self.env_prefix}API_HOST"):
            api_config["host"] = api_host
        
        if api_port := os.getenv(f"{self.env_prefix}API_PORT"):
            try:
                api_config["port"] = int(api_port)
            except ValueError:
                pass
        
        if api_debug := os.getenv(f"{self.env_prefix}API_DEBUG"):
            api_config["debug"] = api_debug.lower() in ("true", "1", "yes", "on")
        
        if api_https := os.getenv(f"{self.env_prefix}API_USE_HTTPS"):
            api_config["use_https"] = api_https.lower() in ("true", "1", "yes", "on")
        
        if cors_origins := os.getenv(f"{self.env_prefix}CORS_ORIGINS"):
            api_config["cors_origins"] = [
                origin.strip() for origin in cors_origins.split(",")
            ]
        
        if api_key := os.getenv(f"{self.env_prefix}API_KEY"):
            api_config["api_key"] = api_key
        
        if rate_limit := os.getenv(f"{self.env_prefix}RATE_LIMIT"):
            api_config["rate_limit"] = rate_limit
        
        if api_config:
            config["api"] = api_config
        
        # Logging configuration
        logging_config = {}
        if log_level := os.getenv(f"{self.env_prefix}LOGGING_LEVEL"):
            logging_config["level"] = log_level
        
        if log_format := os.getenv(f"{self.env_prefix}LOGGING_FORMAT"):
            logging_config["format"] = log_format
        
        if log_file := os.getenv(f"{self.env_prefix}LOGGING_FILE"):
            logging_config["file_path"] = log_file
        
        if log_json := os.getenv(f"{self.env_prefix}LOGGING_JSON"):
            logging_config["json_format"] = log_json.lower() in ("true", "1", "yes", "on")
        
        if logging_config:
            config["logging"] = logging_config
        
        # Security configuration
        security_config = {}
        if secret_key := os.getenv(f"{self.env_prefix}SECRET_KEY"):
            security_config["secret_key"] = secret_key
        
        if jwt_algorithm := os.getenv(f"{self.env_prefix}JWT_ALGORITHM"):
            security_config["jwt_algorithm"] = jwt_algorithm
        
        if jwt_expiration := os.getenv(f"{self.env_prefix}JWT_EXPIRATION_HOURS"):
            try:
                security_config["jwt_expiration_hours"] = int(jwt_expiration)
            except ValueError:
                pass
        
        if allowed_hosts := os.getenv(f"{self.env_prefix}ALLOWED_HOSTS"):
            security_config["allowed_hosts"] = [
                host.strip() for host in allowed_hosts.split(",")
            ]
        
        if api_key_header := os.getenv(f"{self.env_prefix}API_KEY_HEADER"):
            security_config["api_key_header"] = api_key_header
        
        if security_config:
            config["security"] = security_config
        
        return config
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries, with override taking precedence."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result


class ConfigManager:
    """Singleton configuration manager for application-wide config access."""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager."""
        if self._initialized:
            return
        
        self._config: Optional[LightwaveConfig] = None
        self._config_path: Optional[Path] = None
        self._loader = ConfigLoader()
        self._initialized = True
    
    def load_from_file(
        self, 
        file_path: Union[str, Path], 
        allow_env_override: bool = True
    ) -> LightwaveConfig:
        """Load configuration from file."""
        self._config_path = Path(file_path)
        self._config = self._loader.load_from_file(file_path, allow_env_override)
        return self._config
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> LightwaveConfig:
        """Load configuration from dictionary."""
        self._config = self._loader.load_from_dict(config_dict)
        self._config_path = None
        return self._config
    
    def load_from_environment(self) -> LightwaveConfig:
        """Load configuration from environment variables."""
        self._config = self._loader.load_from_environment()
        self._config_path = None
        return self._config
    
    def auto_load(self, search_paths: Optional[List[Union[str, Path]]] = None) -> LightwaveConfig:
        """Automatically load configuration from common paths."""
        if search_paths is None:
            search_paths = [
                "lightwave.yaml",
                "lightwave.yml",
                "config/lightwave.yaml", 
                "config/lightwave.yml",
                "lightwave.json",
                "config/lightwave.json",
                ".lightwave/config.yaml",
                ".lightwave/config.yml",
            ]
        
        # First, try to load from files
        for path in search_paths:
            path = Path(path)
            if path.exists():
                return self.load_from_file(path)
        
        # If no file found, load from environment
        return self.load_from_environment()
    
    def reload(self) -> LightwaveConfig:
        """Reload configuration from the same source."""
        if self._config_path and self._config_path.exists():
            return self.load_from_file(self._config_path)
        else:
            return self.load_from_environment()
    
    def get_config(self) -> LightwaveConfig:
        """Get current configuration, loading defaults if none set."""
        if self._config is None:
            # Try auto-loading first
            try:
                return self.auto_load()
            except (ConfigLoadError, ConfigValidationError):
                # Fall back to default configuration
                self._config = self._create_default_config()
        
        return self._config
    
    def set_config(self, config: LightwaveConfig) -> None:
        """Set configuration manually."""
        self._config = config
        self._config_path = None
    
    def is_loaded(self) -> bool:
        """Check if configuration is loaded."""
        return self._config is not None
    
    def get_config_source(self) -> str:
        """Get description of configuration source."""
        if self._config_path:
            return f"file: {self._config_path}"
        elif self._config:
            return "environment variables"
        else:
            return "default configuration"
    
    def _create_default_config(self) -> LightwaveConfig:
        """Create default configuration."""
        # Detect environment from environment variable
        env_str = os.getenv("LIGHTWAVE_ENVIRONMENT", "development")
        try:
            environment = Environment(env_str.lower())
        except ValueError:
            environment = Environment.DEVELOPMENT
        
        return LightwaveConfig(
            service_name=os.getenv("LIGHTWAVE_SERVICE_NAME", "lightwave-service"),
            version=os.getenv("LIGHTWAVE_VERSION", "1.0.0"),
            environment=environment,
            description="Default Lightwave service configuration",
        )


# Global configuration manager instance
_config_manager = ConfigManager()