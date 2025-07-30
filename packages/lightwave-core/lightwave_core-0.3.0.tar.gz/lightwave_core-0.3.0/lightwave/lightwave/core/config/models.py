"""
Configuration Models for Lightwave Ecosystem.

Enterprise-grade Pydantic models for configuration management across
all Lightwave services. Provides type safety, validation, and 
standardized configuration patterns.
"""

import os
import secrets
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.types import SecretStr


class ConfigValidationError(ValueError):
    """Raised when configuration validation fails."""
    pass


class ConfigLoadError(Exception):
    """Raised when configuration cannot be loaded."""
    pass


class Environment(str, Enum):
    """Environment enumeration for different deployment environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def is_development(self) -> bool:
        return self == Environment.DEVELOPMENT
    
    @property
    def is_staging(self) -> bool:
        return self == Environment.STAGING
    
    @property
    def is_production(self) -> bool:
        return self == Environment.PRODUCTION
    
    @property
    def is_testing(self) -> bool:
        return self == Environment.TESTING


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
    def __str__(self) -> str:
        return self.value


class DatabaseConfig(BaseModel):
    """Database configuration with support for multiple database types."""
    
    url: str = Field(
        default="sqlite:///data.db",
        description="Database connection URL"
    )
    
    driver: Optional[str] = Field(
        default=None,
        description="Database driver (auto-detected if not provided)"
    )
    
    pool_size: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Connection pool size"
    )
    
    max_overflow: int = Field(
        default=10,
        ge=0,
        le=100,
        description="Maximum pool overflow connections"
    )
    
    echo: bool = Field(
        default=False,
        description="Enable SQL query logging"
    )
    
    connect_timeout: int = Field(
        default=30,
        ge=1,
        description="Connection timeout in seconds"
    )
    
    query_timeout: int = Field(
        default=300,
        ge=1,
        description="Query timeout in seconds"
    )
    
    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        """Validate database URL format."""
        if not v or not v.strip():
            raise ConfigValidationError("Database URL cannot be empty")
        
        try:
            parsed = urlparse(v)
            if not parsed.scheme:
                raise ConfigValidationError(f"Invalid database URL format: {v}")
        except Exception as e:
            raise ConfigValidationError(f"Invalid database URL: {e}")
        
        return v
    
    @model_validator(mode='after')
    def auto_detect_driver(self):
        """Auto-detect database driver from URL if not provided."""
        if self.driver:
            return self
        
        if not self.url:
            return self
        
        scheme = urlparse(self.url).scheme
        driver_mapping = {
            "postgresql": "postgresql+psycopg2",
            "postgres": "postgresql+psycopg2", 
            "mysql": "mysql+pymysql",
            "sqlite": "sqlite",
            "oracle": "oracle+cx_oracle",
            "mssql": "mssql+pyodbc",
        }
        
        self.driver = driver_mapping.get(scheme, scheme)
        return self
    
    def to_sqlalchemy_url(self) -> str:
        """Convert to SQLAlchemy-compatible URL."""
        if self.driver and self.driver != urlparse(self.url).scheme:
            parsed = urlparse(self.url)
            return self.url.replace(parsed.scheme, self.driver, 1)
        return self.url
    
    def to_django_config(self) -> Dict[str, Any]:
        """Convert to Django database configuration."""
        parsed = urlparse(self.url)
        
        engine_mapping = {
            "postgresql": "django.db.backends.postgresql",
            "postgres": "django.db.backends.postgresql",
            "mysql": "django.db.backends.mysql",
            "sqlite": "django.db.backends.sqlite3",
            "oracle": "django.db.backends.oracle",
        }
        
        scheme = parsed.scheme
        if "+" in scheme:
            scheme = scheme.split("+")[0]
        
        config = {
            "ENGINE": engine_mapping.get(scheme, "django.db.backends.sqlite3"),
            "NAME": parsed.path.lstrip("/") if parsed.path else "data.db",
        }
        
        if parsed.hostname:
            config.update({
                "HOST": parsed.hostname,
                "PORT": parsed.port or "",
                "USER": parsed.username or "",
                "PASSWORD": parsed.password or "",
            })
        
        return config


class ApiConfig(BaseModel):
    """API server configuration."""
    
    host: str = Field(
        default="127.0.0.1",
        description="API server host"
    )
    
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="API server port"
    )
    
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    use_https: bool = Field(
        default=False,
        description="Use HTTPS protocol"
    )
    
    cors_origins: List[str] = Field(
        default_factory=list,
        description="Allowed CORS origins"
    )
    
    api_key: Optional[str] = Field(
        default=None,
        description="API key for authentication"
    )
    
    rate_limit: Optional[str] = Field(
        default="100/minute",
        description="Rate limiting configuration"
    )
    
    request_timeout: int = Field(
        default=30,
        ge=1,
        description="Request timeout in seconds"
    )
    
    max_request_size: int = Field(
        default=16 * 1024 * 1024,  # 16MB
        ge=1024,
        description="Maximum request size in bytes"
    )
    
    @field_validator("host")
    @classmethod
    def validate_host(cls, v):
        """Validate host format."""
        if not v or not v.strip():
            raise ConfigValidationError("Host cannot be empty")
        return v.strip()
    
    @property
    def base_url(self) -> str:
        """Generate base URL from host and port."""
        protocol = "https" if self.use_https else "http"
        return f"{protocol}://{self.host}:{self.port}"


class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Logging level"
    )
    
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )
    
    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Date format for log messages"
    )
    
    file_path: Optional[str] = Field(
        default=None,
        description="Log file path (None for console only)"
    )
    
    max_bytes: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        ge=1024,
        description="Maximum log file size in bytes"
    )
    
    backup_count: int = Field(
        default=3,
        ge=0,
        description="Number of backup log files to keep"
    )
    
    json_format: bool = Field(
        default=False,
        description="Use JSON format for structured logging"
    )
    
    include_trace: bool = Field(
        default=False,
        description="Include stack trace in error logs"
    )
    
    sensitive_fields: List[str] = Field(
        default_factory=lambda: ["password", "token", "api_key", "secret"],
        description="Fields to mask in logs"
    )
    
    @field_validator("level")
    @classmethod
    def validate_level(cls, v):
        """Validate log level."""
        if isinstance(v, str):
            try:
                return LogLevel(v.upper())
            except ValueError:
                valid_levels = [level.value for level in LogLevel]
                raise ConfigValidationError(
                    f"Invalid log level: {v}. Valid levels: {valid_levels}"
                )
        return v


class SecurityConfig(BaseModel):
    """Security configuration."""
    
    secret_key: str = Field(
        description="Secret key for cryptographic operations"
    )
    
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    
    jwt_expiration_hours: int = Field(
        default=24,
        ge=1,
        description="JWT token expiration in hours"
    )
    
    password_min_length: int = Field(
        default=8,
        ge=6,
        description="Minimum password length"
    )
    
    allowed_hosts: List[str] = Field(
        default_factory=list,
        description="Allowed hosts for API access"
    )
    
    api_key_header: str = Field(
        default="X-API-Key",
        description="Header name for API key authentication"
    )
    
    cors_max_age: int = Field(
        default=86400,  # 24 hours
        ge=0,
        description="CORS preflight cache duration in seconds"
    )
    
    session_timeout: int = Field(
        default=1800,  # 30 minutes
        ge=60,
        description="Session timeout in seconds"
    )
    
    rate_limit_storage: str = Field(
        default="memory",
        description="Rate limit storage backend (memory/redis)"
    )
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v):
        """Validate secret key strength."""
        if not v or not v.strip():
            raise ConfigValidationError("Secret key cannot be empty")
        
        v = v.strip()
        if len(v) < 16:
            raise ConfigValidationError("Secret key must be at least 16 characters long")
        
        return v
    
    @staticmethod
    def generate_secret_key(length: int = 32) -> str:
        """Generate a cryptographically secure secret key."""
        return secrets.token_urlsafe(length)


class LightwaveConfig(BaseModel):
    """Main Lightwave configuration model."""
    
    # Service identification
    service_name: str = Field(
        description="Name of the service"
    )
    
    version: str = Field(
        description="Service version"
    )
    
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Deployment environment"
    )
    
    description: Optional[str] = Field(
        default=None,
        description="Service description"
    )
    
    # Configuration sections
    database: DatabaseConfig = Field(
        default_factory=DatabaseConfig,
        description="Database configuration"
    )
    
    api: ApiConfig = Field(
        default_factory=ApiConfig,
        description="API server configuration"
    )
    
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig,
        description="Logging configuration"
    )
    
    security: SecurityConfig = Field(
        default=None,
        description="Security configuration"
    )
    
    # Additional settings
    features: Dict[str, bool] = Field(
        default_factory=dict,
        description="Feature flags"
    )
    
    integrations: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Third-party integration settings"
    )
    
    custom: Dict[str, Any] = Field(
        default_factory=dict,
        description="Custom application-specific settings"
    )
    
    @field_validator("service_name")
    @classmethod
    def validate_service_name(cls, v):
        """Validate service name."""
        if not v or not v.strip():
            raise ConfigValidationError("Service name cannot be empty")
        return v.strip()
    
    @field_validator("version")
    @classmethod
    def validate_version(cls, v):
        """Validate version format."""
        if not v or not v.strip():
            raise ConfigValidationError("Version cannot be empty")
        return v.strip()
    
    @model_validator(mode='after')
    def configure_environment_defaults(self):
        """Configure defaults based on environment."""
        # Configure API defaults based on environment
        if self.environment == Environment.DEVELOPMENT:
            self.api.debug = True
        elif self.environment in (Environment.STAGING, Environment.PRODUCTION):
            self.api.debug = False
        
        # Configure logging defaults based on environment
        if self.environment == Environment.DEVELOPMENT:
            self.logging.level = LogLevel.DEBUG
        elif self.environment == Environment.STAGING:
            self.logging.level = LogLevel.INFO
        elif self.environment == Environment.PRODUCTION:
            self.logging.level = LogLevel.WARNING
        
        # Generate security config if not provided
        if not self.security:
            self.security = SecurityConfig(
                secret_key=SecurityConfig.generate_secret_key()
            )
        
        return self
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled."""
        return self.features.get(feature_name, False)
    
    def get_integration_config(self, integration_name: str) -> Dict[str, Any]:
        """Get configuration for a specific integration."""
        return self.integrations.get(integration_name, {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump(by_alias=True, exclude_none=False)
    
    model_config = {
        "use_enum_values": True,
        "validate_assignment": True,
        "extra": "forbid",  # Prevent additional fields
        "json_schema_extra": {
            "example": {
                "service_name": "my-lightwave-service",
                "version": "1.0.0",
                "environment": "development",
                "description": "A sample Lightwave service",
                "database": {
                    "url": "postgresql://user:pass@localhost:5432/mydb",
                    "pool_size": 10
                },
                "api": {
                    "host": "0.0.0.0",
                    "port": 8000,
                    "debug": True
                },
                "logging": {
                    "level": "INFO",
                    "file_path": "/var/log/service.log"
                },
                "security": {
                    "secret_key": "your-secret-key-here",
                    "jwt_expiration_hours": 24
                },
                "features": {
                    "feature_a": True,
                    "feature_b": False
                }
            }
        }
    }