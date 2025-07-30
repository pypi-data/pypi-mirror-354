"""
Lightwave Shared Core Library.

A comprehensive core library for the Lightwave ecosystem providing:
- Task and workflow management models
- Configuration management system
- API client functionality  
- Data validation utilities
- Formatting and subdomain helpers
- Testing infrastructure

This package follows enterprise software development patterns and provides
a solid foundation for building Lightwave applications.
"""

from .core.models import BaseModel, Task, TaskStatus, TaskPriority, SubTask
from .core.services import ApiClient, TaskService
from .core.utils import format_currency, format_date, extract_subdomain, validate_subdomain

# Configuration system
from .core.config import (
    LightwaveConfig,
    DatabaseConfig,
    ApiConfig,
    LoggingConfig,
    SecurityConfig,
    Environment,
    ConfigValidationError,
    ConfigLoadError,
    load_config,
    get_config,
    set_config_path,
    ConfigManager,
    ConfigLoader,
)

__version__ = "0.3.0"

__all__ = [
    # Models
    "BaseModel",
    "Task", 
    "TaskStatus",
    "TaskPriority", 
    "SubTask",
    
    # Configuration
    "LightwaveConfig",
    "DatabaseConfig",
    "ApiConfig", 
    "LoggingConfig",
    "SecurityConfig",
    "Environment",
    "ConfigValidationError",
    "ConfigLoadError",
    "load_config",
    "get_config",
    "set_config_path",
    "ConfigManager",
    "ConfigLoader",
    
    # Services
    "ApiClient",
    "TaskService",
    
    # Utils
    "format_currency",
    "format_date", 
    "extract_subdomain",
    "validate_subdomain",
]