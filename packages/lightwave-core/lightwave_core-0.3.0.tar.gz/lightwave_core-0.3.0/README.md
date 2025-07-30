# Lightwave Core Library

[![Tests](https://github.com/kiwi-dev-la/lightwave-core/actions/workflows/test.yml/badge.svg)](https://github.com/kiwi-dev-la/lightwave-core/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/lightwave-core.svg)](https://badge.fury.io/py/lightwave-core)
[![Python Versions](https://img.shields.io/pypi/pyversions/lightwave-core.svg)](https://pypi.org/project/lightwave-core/)
[![Code Coverage](https://codecov.io/gh/kiwi-dev-la/lightwave-core/branch/main/graph/badge.svg)](https://codecov.io/gh/kiwi-dev-la/lightwave-core)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

Core library for the Lightwave task and project management system. This library provides the fundamental functionality, models, and services used by the Lightwave CLI and other tools.

## Features

- ⚙️ **Configuration Management** ⭐ **NEW**
  - ✅ Multi-source configuration (YAML/JSON files, environment variables, defaults)
  - ✅ Environment-specific settings (development/staging/production)
  - ✅ Database configuration (PostgreSQL, MySQL, SQLite)
  - ✅ API server configuration (FastAPI, Django REST)
  - ✅ Security configuration with secret key generation
  - ✅ Logging configuration with multiple output formats
  - ✅ Pydantic v2 validation and type safety
- 🎯 **Task Management**
  - ✅ Create and manage tasks with subtasks
  - ✅ Track dependencies and blockers  
  - ✅ Priority-based task organization (LOW → MEDIUM → HIGH → CRITICAL)
  - ✅ Status tracking (PENDING → IN_PROGRESS → DONE, etc.)
  - ✅ Acceptance criteria management
  - ✅ Time estimation and tracking
- 🔧 **Core Models**
  - ✅ Pydantic-based BaseModel with API serialization
  - ✅ Comprehensive Task and SubTask models
  - ✅ Type-safe enumerations (TaskStatus, TaskPriority)
  - ✅ Automatic timestamp management
- 🌐 **API Client**
  - ✅ HTTP client with automatic retry logic
  - ✅ Pydantic model validation
  - ✅ Authentication handling
  - ✅ Error handling and logging
- 🛠 **Utilities**
  - ✅ Date and currency formatting
  - ✅ Subdomain and domain utilities  
  - ✅ Host configuration management
- 🔒 **Type Safety**
  - ✅ Full type hints coverage
  - ✅ Pydantic v2 models for validation
  - ✅ MyPy compatibility
- 🧪 **Quality Assurance**
  - ✅ 96%+ test coverage on core models
  - ✅ Comprehensive test suite with pytest
  - ✅ Enterprise-grade error handling

## Quick Start

### Installation

Using uv (recommended):
```bash
uv install lightwave-core
```

For development installation with all extras:
```bash
uv install "lightwave-core[all-dev]"
```

### Basic Usage

#### Configuration Management

```python
from lightwave import get_config, load_config, LightwaveConfig

# Load configuration from file
config = load_config("config.yaml")

# Or get current configuration (auto-loads from common paths)
config = get_config()

# Access configuration sections
db_url = config.database.url
api_port = config.api.port
log_level = config.logging.level
secret_key = config.security.secret_key

# Check environment
if config.environment.is_production:
    print("Running in production mode")

# Create configuration programmatically
config = LightwaveConfig(
    service_name="my-lightwave-service",
    version="1.0.0",
    environment="development"
)
```

#### Task Management

```python
from lightwave import Task, TaskStatus, TaskPriority
from datetime import datetime

# Create a new task
task = Task(
    id=1,
    title="Implement user authentication",
    description="Add OAuth2 authentication to the API",
    priority=TaskPriority.HIGH
)

# Add subtasks
oauth_subtask = task.add_subtask(
    title="Set up OAuth2 provider",
    description="Configure Auth0 integration"
)

login_subtask = task.add_subtask(
    title="Implement login endpoints", 
    description="Create /login and /callback routes"
)

# Add dependencies between subtasks
jwt_subtask = task.add_subtask(
    title="Add token validation",
    description="Implement JWT validation middleware",
    dependencies=[oauth_subtask.id]  # Depends on OAuth setup
)

# Update task status
task.update_status(TaskStatus.IN_PROGRESS)

# Add acceptance criteria
task.add_acceptance_criterion("Must support Google OAuth2")
task.add_acceptance_criterion("Must have comprehensive tests")
task.add_acceptance_criterion("Must pass security review")

# Track progress
print(f"Task completion: {task.get_completion_percentage()}%")

# Get ready-to-work subtasks (no unmet dependencies)
ready_tasks = task.get_ready_subtasks()
print(f"Ready to work on: {[st.title for st in ready_tasks]}")
```

#### Configuration Files

Create a `lightwave.yaml` configuration file:

```yaml
# Lightwave Configuration
service_name: my-lightwave-app
version: 1.0.0
environment: development
description: My awesome Lightwave application

# Database Configuration
database:
  url: postgresql://user:pass@localhost:5432/mydb
  pool_size: 10
  max_overflow: 20
  echo: false

# API Configuration  
api:
  host: 0.0.0.0
  port: 8000
  debug: true
  cors_origins:
    - http://localhost:3000
    - https://myapp.com
  
# Logging Configuration
logging:
  level: DEBUG
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file_path: /var/log/app.log
  
# Security Configuration
security:
  secret_key: your-super-secret-key-here
  jwt_expiration_hours: 24
  allowed_hosts:
    - localhost
    - myapp.com

# Feature Flags
features:
  new_ui_enabled: true
  beta_features: false

# Third-party Integrations
integrations:
  redis:
    host: localhost
    port: 6379
    db: 0
```

### Advanced Features

#### API Client with Pydantic Models

```python
from lightwave import ApiClient, Task

# Create API client with authentication
client = ApiClient(
    base_url="https://api.example.com",
    api_key="your-api-key",
    timeout=30.0
)

# Make requests with automatic model validation
task_data = {
    "id": 1,
    "title": "New API Task", 
    "description": "Task created via API",
    "priority": "high"
}

# POST request with automatic Task model validation
created_task = client.post(
    "/tasks",
    data=task_data,
    response_model=Task
)

# GET request with model validation
tasks = client.get("/tasks", response_model=Task)

# The client handles:
# - Automatic retries on failure
# - JSON serialization/deserialization  
# - Pydantic model validation
# - Authentication headers
# - Error handling
```

#### Data Formatting Utilities

```python
from lightwave.core.utils import format_currency, format_date
from datetime import datetime

# Currency formatting
amount = format_currency(1234.56)  # "$1,234.56"
euro_amount = format_currency(1000, "EUR")  # "$1,000.00 EUR"

# Date formatting
now = datetime.now()
iso_date = format_date(now)  # "2024-01-15"  
us_date = format_date(now, "%m/%d/%Y")  # "01/15/2024"
```

#### Sprint Analytics

```python
from lightwave.core import SprintService
from datetime import datetime, timedelta

# Create sprint service
sprint_service = SprintService()

# Create a new sprint
sprint = sprint_service.create_sprint(
    name="Sprint 1",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    capacity=80  # story points
)

# Add tasks to sprint
sprint_service.add_tasks_to_sprint(
    sprint_id=sprint.id,
    task_ids=[task.id for task in tasks]
)

# Get sprint metrics
metrics = sprint_service.get_metrics(sprint.id)
print(f"Velocity: {metrics.velocity}")
print(f"Burndown: {metrics.burndown_chart}")
print(f"Completion: {metrics.completion_percentage}%")
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kiwi-dev-la/lightwave-core.git
   cd lightwave-core
   ```

2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   uv pip install -e ".[dev,test]"
   ```

5. Install pre-commit hooks:
   ```bash
   uv pip run pre-commit install
   ```

### Quality Checks

Run all quality checks:

```bash
# Format code
uv pip run ruff format .

# Run linter
uv pip run ruff check .

# Run type checker
uv pip run mypy src

# Run tests with coverage
uv pip run pytest --cov=src/lightwave
```

### Publishing

1. Update version in `pyproject.toml`
2. Create and push a new tag:
   ```bash
   git tag v0.1.4
   git push origin v0.1.4
   ```
3. Create a new release on GitHub
4. CI/CD will automatically:
   - Run all tests
   - Build the package
   - Publish to PyPI and GitHub Packages

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run quality checks:
   ```bash
   ruff format .
   ruff check .
   mypy src
   pytest
   ```
5. Commit your changes:
   ```bash
   git commit -m "feat: add your feature"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Submit a pull request

## License

Proprietary - All rights reserved

## Related Projects

- [lightwave-cli](https://github.com/kiwi-dev-la/lightwave-cli) - Command-line interface for Lightwave
- [lightwave-web](https://github.com/kiwi-dev-la/lightwave-web) - Web interface for Lightwave
- [lightwave-docs](https://github.com/kiwi-dev-la/lightwave-docs) - Documentation site
