"""Tests for the boilerplate templates used for core agents."""

import os
import pytest
from pathlib import Path
from typing import Dict, Any

from lightwave_ai.agents.boilerplate_agent import (
    BoilerplateAgent,
    BoilerplateConfig,
    BoilerplateResult
)

@pytest.mark.unit
class TestBoilerplateTemplates:
    """Test suite for boilerplate templates."""
    
    @pytest.fixture
    def test_template_dir(self, tmp_path) -> Path:
        """Create a temporary directory for test templates."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        return template_dir
    
    @pytest.fixture
    def test_output_dir(self, tmp_path) -> Path:
        """Create a temporary directory for test output."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        return output_dir
    
    @pytest.fixture
    def basic_config(self) -> Dict[str, Any]:
        """Create a basic template configuration."""
        return {
            "variables": [
                {
                    "name": "agent_name",
                    "description": "Name of the agent",
                    "default": "test_agent"
                },
                {
                    "name": "agent_type",
                    "description": "Type of agent to create",
                    "default": "core"
                }
            ],
            "structure": [
                {
                    "type": "directory",
                    "name": "src",
                    "children": [
                        {
                            "type": "file",
                            "name": "main.py",
                            "template": True,
                            "content": """
from typing import Dict, Any
from pydantic_ai import Agent

class {{agent_name}}(Agent):
    \"\"\"{{agent_type}} agent implementation.\"\"\"
    
    def __init__(self):
        super().__init__()
"""
                        }
                    ]
                },
                {
                    "type": "file",
                    "name": "requirements.txt",
                    "content": """
pydantic-ai>=0.1.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
"""
                }
            ]
        }
    
    def test_template_creation(self, test_template_dir: Path, basic_config: Dict[str, Any]):
        """Test creating a new template from configuration."""
        agent = BoilerplateAgent()
        config = BoilerplateConfig(**basic_config)
        
        template_dir = agent.create_template(test_template_dir, config)
        
        # Verify template structure
        assert (template_dir / "src").is_dir()
        assert (template_dir / "src" / "main.py").is_file()
        assert (template_dir / "requirements.txt").is_file()
        assert (template_dir / "boilerplate.yml").is_file()
    
    def test_template_generation(self, test_template_dir: Path, test_output_dir: Path, basic_config: Dict[str, Any]):
        """Test generating a project from a template."""
        agent = BoilerplateAgent()
        config = BoilerplateConfig(**basic_config)
        
        # Create template
        template_dir = agent.create_template(test_template_dir, config)
        
        # Generate project
        variables = {
            "agent_name": "CustomAgent",
            "agent_type": "specialized"
        }
        result = agent.run_boilerplate(template_dir, test_output_dir, variables)
        
        # Verify generated files
        assert isinstance(result, BoilerplateResult)
        assert (test_output_dir / "src" / "main.py").is_file()
        assert (test_output_dir / "requirements.txt").is_file()
        
        # Check content substitution
        with open(test_output_dir / "src" / "main.py") as f:
            content = f.read()
            assert "class CustomAgent(Agent):" in content
            assert "specialized agent implementation" in content
    
    def test_template_validation(self, test_template_dir: Path, basic_config: Dict[str, Any]):
        """Test template validation."""
        agent = BoilerplateAgent()
        
        # Test with invalid configuration
        invalid_config = basic_config.copy()
        invalid_config["variables"].append({
            "name": "invalid_var"  # Missing required fields
        })
        
        with pytest.raises(ValueError):
            BoilerplateConfig(**invalid_config)
    
    def test_template_generation_with_missing_variables(self, test_template_dir: Path, test_output_dir: Path, basic_config: Dict[str, Any]):
        """Test template generation with missing variables."""
        agent = BoilerplateAgent()
        config = BoilerplateConfig(**basic_config)
        
        # Create template
        template_dir = agent.create_template(test_template_dir, config)
        
        # Generate project with missing variable
        variables = {
            "agent_name": "CustomAgent"
            # Missing agent_type
        }
        
        # Should use default value for missing variable
        result = agent.run_boilerplate(template_dir, test_output_dir, variables)
        
        with open(test_output_dir / "src" / "main.py") as f:
            content = f.read()
            assert "core agent implementation" in content  # Default value used
    
    def test_template_file_permissions(self, test_template_dir: Path, test_output_dir: Path, basic_config: Dict[str, Any]):
        """Test that generated files have correct permissions."""
        agent = BoilerplateAgent()
        config = BoilerplateConfig(**basic_config)
        
        # Create and generate template
        template_dir = agent.create_template(test_template_dir, config)
        result = agent.run_boilerplate(template_dir, test_output_dir)
        
        # Check permissions (should be readable and writable by owner)
        main_py = test_output_dir / "src" / "main.py"
        assert os.access(main_py, os.R_OK | os.W_OK)
        
        # Ensure Python files are executable
        assert os.access(main_py, os.X_OK) 