"""
Enterprise-grade tests for configuration management system.

Following TDD principles with comprehensive coverage of configuration
loading, validation, environment handling, and security patterns.
"""

import os
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
from unittest.mock import patch, mock_open
from pydantic import ValidationError

from lightwave.core.config import (
    ConfigManager,
    DatabaseConfig,
    ApiConfig,
    LoggingConfig,
    SecurityConfig,
    LightwaveConfig,
    ConfigValidationError,
    load_config,
    get_config,
    set_config_path,
    ConfigLoader,
    Environment
)


class TestDatabaseConfig:
    """Test database configuration model."""
    
    def test_database_config_creation(self):
        """Test basic database config creation."""
        db_config = DatabaseConfig(
            url="postgresql://user:pass@localhost:5432/db",
            driver="postgresql+psycopg2",
            pool_size=10,
            max_overflow=20
        )
        
        assert db_config.url == "postgresql://user:pass@localhost:5432/db"
        assert db_config.driver == "postgresql+psycopg2"
        assert db_config.pool_size == 10
        assert db_config.max_overflow == 20
        assert db_config.echo is False  # default
    
    def test_database_config_with_defaults(self):
        """Test database config with default values."""
        db_config = DatabaseConfig(url="sqlite:///test.db")
        
        assert db_config.url == "sqlite:///test.db"
        assert db_config.driver == "sqlite"  # auto-detected
        assert db_config.pool_size == 5  # default
        assert db_config.max_overflow == 10  # default
        assert db_config.echo is False
    
    def test_database_config_validation(self):
        """Test database config validation."""
        with pytest.raises(ValidationError):
            DatabaseConfig(url="")  # empty URL should fail
        
        with pytest.raises(ValidationError):
            DatabaseConfig(url="invalid-url")  # invalid URL format
    
    def test_database_config_connection_string_parsing(self):
        """Test connection string parsing for different databases."""
        # PostgreSQL
        pg_config = DatabaseConfig(url="postgresql://user:pass@localhost:5432/mydb")
        assert pg_config.driver == "postgresql+psycopg2"
        
        # MySQL
        mysql_config = DatabaseConfig(url="mysql://user:pass@localhost:3306/mydb")
        assert mysql_config.driver == "mysql+pymysql"
        
        # SQLite
        sqlite_config = DatabaseConfig(url="sqlite:///path/to/db.sqlite")
        assert sqlite_config.driver == "sqlite"
    
    def test_database_config_to_sqlalchemy_url(self):
        """Test conversion to SQLAlchemy URL."""
        db_config = DatabaseConfig(
            url="postgresql://user:pass@localhost:5432/db",
            driver="postgresql+psycopg2"
        )
        
        sqlalchemy_url = db_config.to_sqlalchemy_url()
        assert str(sqlalchemy_url).startswith("postgresql+psycopg2://")


class TestApiConfig:
    """Test API configuration model."""
    
    def test_api_config_creation(self):
        """Test basic API config creation."""
        api_config = ApiConfig(
            host="0.0.0.0",
            port=8000,
            debug=True,
            cors_origins=["http://localhost:3000"],
            api_key="test-key-123"
        )
        
        assert api_config.host == "0.0.0.0"
        assert api_config.port == 8000
        assert api_config.debug is True
        assert api_config.cors_origins == ["http://localhost:3000"]
        assert api_config.api_key == "test-key-123"
    
    def test_api_config_with_defaults(self):
        """Test API config with default values."""
        api_config = ApiConfig()
        
        assert api_config.host == "127.0.0.1"
        assert api_config.port == 8000
        assert api_config.debug is False
        assert api_config.cors_origins == []
        assert api_config.api_key is None
    
    def test_api_config_validation(self):
        """Test API config validation."""
        with pytest.raises(ValidationError):
            ApiConfig(port=-1)  # invalid port
        
        with pytest.raises(ValidationError):
            ApiConfig(port=70000)  # port too high
        
        with pytest.raises(ValidationError):
            ApiConfig(host="")  # empty host
    
    def test_api_config_base_url_property(self):
        """Test base URL property generation."""
        api_config = ApiConfig(host="localhost", port=8080)
        assert api_config.base_url == "http://localhost:8080"
        
        api_config_https = ApiConfig(host="api.example.com", port=443, use_https=True)
        assert api_config_https.base_url == "https://api.example.com:443"


class TestLoggingConfig:
    """Test logging configuration model."""
    
    def test_logging_config_creation(self):
        """Test basic logging config creation."""
        log_config = LoggingConfig(
            level="DEBUG",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            file_path="/var/log/app.log",
            max_bytes=10485760,  # 10MB
            backup_count=5
        )
        
        assert log_config.level == "DEBUG"
        assert log_config.format == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        assert log_config.file_path == "/var/log/app.log"
        assert log_config.max_bytes == 10485760
        assert log_config.backup_count == 5
    
    def test_logging_config_defaults(self):
        """Test logging config defaults."""
        log_config = LoggingConfig()
        
        assert log_config.level == "INFO"
        assert "%(asctime)s" in log_config.format
        assert log_config.file_path is None
        assert log_config.max_bytes == 10485760
        assert log_config.backup_count == 3
    
    def test_logging_config_validation(self):
        """Test logging config validation."""
        with pytest.raises(ValidationError):
            LoggingConfig(level="INVALID")  # invalid log level
        
        with pytest.raises(ValidationError):
            LoggingConfig(max_bytes=-1)  # negative max_bytes
        
        with pytest.raises(ValidationError):
            LoggingConfig(backup_count=-1)  # negative backup_count


class TestSecurityConfig:
    """Test security configuration model."""
    
    def test_security_config_creation(self):
        """Test basic security config creation."""
        security_config = SecurityConfig(
            secret_key="super-secret-key-12345",
            jwt_algorithm="HS256",
            jwt_expiration_hours=24,
            allowed_hosts=["localhost", "127.0.0.1"],
            api_key_header="X-API-Key"
        )
        
        assert security_config.secret_key == "super-secret-key-12345"
        assert security_config.jwt_algorithm == "HS256"
        assert security_config.jwt_expiration_hours == 24
        assert security_config.allowed_hosts == ["localhost", "127.0.0.1"]
        assert security_config.api_key_header == "X-API-Key"
    
    def test_security_config_validation(self):
        """Test security config validation."""
        with pytest.raises(ValidationError):
            SecurityConfig(secret_key="")  # empty secret key
        
        with pytest.raises(ValidationError):
            SecurityConfig(secret_key="short")  # too short
        
        with pytest.raises(ValidationError):
            SecurityConfig(jwt_expiration_hours=-1)  # negative expiration
    
    def test_security_config_generate_secret_key(self):
        """Test secret key generation."""
        key = SecurityConfig.generate_secret_key()
        assert len(key) >= 32
        assert isinstance(key, str)
        
        # Should generate different keys each time
        key2 = SecurityConfig.generate_secret_key()
        assert key != key2


class TestLightwaveConfig:
    """Test main Lightwave configuration model."""
    
    def test_lightwave_config_creation(self):
        """Test complete Lightwave config creation."""
        config = LightwaveConfig(
            environment=Environment.DEVELOPMENT,
            service_name="test-service",
            version="1.0.0",
            database=DatabaseConfig(url="sqlite:///test.db"),
            api=ApiConfig(port=8080),
            logging=LoggingConfig(level="DEBUG"),
            security=SecurityConfig(secret_key="test-secret-key-12345")
        )
        
        assert config.environment == Environment.DEVELOPMENT
        assert config.service_name == "test-service"
        assert config.version == "1.0.0"
        assert config.database.url == "sqlite:///test.db"
        assert config.api.port == 8080
        assert config.logging.level == "DEBUG"
        assert config.security.secret_key == "test-secret-key-12345"
    
    def test_lightwave_config_with_defaults(self):
        """Test config with default sub-configs."""
        config = LightwaveConfig(
            service_name="test-service",
            version="1.0.0"
        )
        
        # Should create default sub-configs
        assert config.database is not None
        assert config.api is not None
        assert config.logging is not None
        assert config.security is not None
        
        # Should use sensible defaults
        assert config.environment == Environment.DEVELOPMENT
        assert config.database.url == "sqlite:///data.db"
        assert config.api.port == 8000
        assert config.logging.level == "DEBUG"  # DEBUG in development
    
    def test_lightwave_config_validation(self):
        """Test main config validation."""
        with pytest.raises(ValidationError):
            LightwaveConfig(service_name="", version="1.0.0")  # empty service name
        
        with pytest.raises(ValidationError):
            LightwaveConfig(service_name="test", version="")  # empty version


class TestConfigLoader:
    """Test configuration loading functionality."""
    
    def test_load_from_dict(self):
        """Test loading config from dictionary."""
        config_dict = {
            "service_name": "test-service",
            "version": "1.0.0",
            "environment": "production",
            "database": {
                "url": "postgresql://user:pass@localhost:5432/db",
                "pool_size": 20
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8080,
                "debug": False
            },
            "logging": {
                "level": "INFO",
                "file_path": "/var/log/app.log"
            },
            "security": {
                "secret_key": "production-secret-key-12345",
                "allowed_hosts": ["api.example.com"]
            }
        }
        
        loader = ConfigLoader()
        config = loader.load_from_dict(config_dict)
        
        assert config.service_name == "test-service"
        assert config.version == "1.0.0"
        assert config.environment == Environment.PRODUCTION
        assert config.database.url == "postgresql://user:pass@localhost:5432/db"
        assert config.database.pool_size == 20
        assert config.api.host == "0.0.0.0"
        assert config.api.port == 8080
        assert config.logging.level == "INFO"
        assert config.security.secret_key == "production-secret-key-12345"
    
    def test_load_from_yaml_file(self, temp_dir):
        """Test loading config from YAML file."""
        yaml_content = """
service_name: yaml-service
version: 2.0.0
environment: staging
database:
  url: postgresql://localhost:5432/yaml_db
  pool_size: 15
api:
  port: 9000
  debug: true
logging:
  level: WARNING
security:
  secret_key: yaml-secret-key-12345
"""
        
        yaml_file = temp_dir / "config.yaml"
        yaml_file.write_text(yaml_content)
        
        loader = ConfigLoader()
        config = loader.load_from_file(str(yaml_file))
        
        assert config.service_name == "yaml-service"
        assert config.version == "2.0.0"
        assert config.environment == Environment.STAGING
        assert config.database.url == "postgresql://localhost:5432/yaml_db"
        assert config.api.port == 9000
        assert config.logging.level == "WARNING"
    
    def test_load_from_json_file(self, temp_dir):
        """Test loading config from JSON file."""
        import json
        
        config_dict = {
            "service_name": "json-service",
            "version": "3.0.0",
            "database": {"url": "sqlite:///json.db"},
            "api": {"port": 7000},
            "security": {"secret_key": "json-secret-key-12345"}
        }
        
        json_file = temp_dir / "config.json"
        json_file.write_text(json.dumps(config_dict, indent=2))
        
        loader = ConfigLoader()
        config = loader.load_from_file(str(json_file))
        
        assert config.service_name == "json-service"
        assert config.version == "3.0.0"
        assert config.database.url == "sqlite:///json.db"
        assert config.api.port == 7000
    
    @patch.dict(os.environ, {
        "LIGHTWAVE_SERVICE_NAME": "env-service",
        "LIGHTWAVE_VERSION": "4.0.0",
        "LIGHTWAVE_ENVIRONMENT": "production",
        "LIGHTWAVE_DATABASE_URL": "postgresql://env:pass@localhost:5432/env_db",
        "LIGHTWAVE_API_PORT": "6000",
        "LIGHTWAVE_LOGGING_LEVEL": "ERROR",
        "LIGHTWAVE_SECRET_KEY": "env-secret-key-12345"
    })
    def test_load_from_environment(self):
        """Test loading config from environment variables."""
        loader = ConfigLoader()
        config = loader.load_from_environment()
        
        assert config.service_name == "env-service"
        assert config.version == "4.0.0"
        assert config.environment == Environment.PRODUCTION
        assert config.database.url == "postgresql://env:pass@localhost:5432/env_db"
        assert config.api.port == 6000
        assert config.logging.level == "ERROR"
        assert config.security.secret_key == "env-secret-key-12345"
    
    def test_environment_variable_override(self, temp_dir):
        """Test environment variables override file config."""
        # Create base config file
        config_dict = {
            "service_name": "file-service",
            "version": "1.0.0",
            "api": {"port": 8000},
            "security": {"secret_key": "file-secret-key"}
        }
        
        import json
        config_file = temp_dir / "config.json"
        config_file.write_text(json.dumps(config_dict))
        
        # Override with environment variables
        with patch.dict(os.environ, {
            "LIGHTWAVE_API_PORT": "9999",
            "LIGHTWAVE_SECRET_KEY": "env-override-key"
        }):
            loader = ConfigLoader()
            config = loader.load_from_file(str(config_file), allow_env_override=True)
            
            assert config.service_name == "file-service"  # from file
            assert config.api.port == 9999  # from env override
            assert config.security.secret_key == "env-override-key"  # from env override
    
    def test_config_validation_error_on_invalid_file(self, temp_dir):
        """Test validation error with invalid config file."""
        invalid_config = {
            "service_name": "",  # invalid empty name
            "version": "1.0.0"
        }
        
        import json
        config_file = temp_dir / "invalid.json"
        config_file.write_text(json.dumps(invalid_config))
        
        loader = ConfigLoader()
        with pytest.raises(ConfigValidationError):
            loader.load_from_file(str(config_file))


class TestConfigManager:
    """Test configuration manager functionality."""
    
    def test_config_manager_singleton(self):
        """Test ConfigManager is a singleton."""
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        assert manager1 is manager2
    
    def test_config_manager_load_and_get(self, temp_dir):
        """Test loading and retrieving config."""
        config_dict = {
            "service_name": "manager-test",
            "version": "1.0.0",
            "api": {"port": 5000}
        }
        
        import json
        config_file = temp_dir / "manager_config.json"
        config_file.write_text(json.dumps(config_dict))
        
        manager = ConfigManager()
        manager.load_from_file(str(config_file))
        
        config = manager.get_config()
        assert config.service_name == "manager-test"
        assert config.api.port == 5000
    
    def test_config_manager_get_without_load(self):
        """Test getting config without loading returns default."""
        manager = ConfigManager()
        manager._config = None  # Reset
        
        config = manager.get_config()
        assert config is not None
        assert config.service_name == "lightwave-service"  # default
    
    def test_config_manager_environment_detection(self):
        """Test automatic environment detection."""
        # Test development (default)
        with patch.dict(os.environ, {}, clear=True):
            manager = ConfigManager()
            config = manager._create_default_config()
            assert config.environment == Environment.DEVELOPMENT
        
        # Test production
        with patch.dict(os.environ, {"LIGHTWAVE_ENVIRONMENT": "production"}):
            manager = ConfigManager()
            config = manager._create_default_config()
            assert config.environment == Environment.PRODUCTION


class TestModuleLevelFunctions:
    """Test module-level convenience functions."""
    
    def test_load_config_function(self, temp_dir):
        """Test load_config convenience function."""
        config_dict = {
            "service_name": "function-test",
            "version": "1.0.0"
        }
        
        import json
        config_file = temp_dir / "function_config.json"
        config_file.write_text(json.dumps(config_dict))
        
        config = load_config(str(config_file))
        assert config.service_name == "function-test"
    
    def test_get_config_function(self):
        """Test get_config convenience function."""
        config = get_config()
        assert config is not None
        assert hasattr(config, 'service_name')
    
    def test_set_config_path_function(self, temp_dir):
        """Test set_config_path convenience function."""
        config_dict = {
            "service_name": "path-test",
            "version": "1.0.0"
        }
        
        import json
        config_file = temp_dir / "path_config.json"
        config_file.write_text(json.dumps(config_dict))
        
        set_config_path(str(config_file))
        config = get_config()
        assert config.service_name == "path-test"


class TestConfigEnvironments:
    """Test configuration for different environments."""
    
    def test_development_environment_defaults(self):
        """Test development environment has appropriate defaults."""
        config = LightwaveConfig(
            environment=Environment.DEVELOPMENT,
            service_name="dev-test",
            version="1.0.0"
        )
        
        assert config.api.debug is True  # debug enabled in dev
        assert config.logging.level == "DEBUG"  # verbose logging in dev
        assert "sqlite" in config.database.url  # local db in dev
    
    def test_production_environment_defaults(self):
        """Test production environment has secure defaults."""
        config = LightwaveConfig(
            environment=Environment.PRODUCTION,
            service_name="prod-test",
            version="1.0.0"
        )
        
        assert config.api.debug is False  # debug disabled in prod
        assert config.logging.level == "WARNING"  # limited logging in prod
        assert len(config.security.secret_key) >= 32  # strong secret in prod
    
    def test_staging_environment_balanced_defaults(self):
        """Test staging environment balances dev and prod."""
        config = LightwaveConfig(
            environment=Environment.STAGING,
            service_name="staging-test",
            version="1.0.0"
        )
        
        assert config.api.debug is False  # debug disabled
        assert config.logging.level == "INFO"  # moderate logging