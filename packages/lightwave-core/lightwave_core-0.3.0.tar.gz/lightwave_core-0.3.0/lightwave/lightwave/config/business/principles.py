# core/principles.py

"""
Core Principles Module for Lightwave Media LLC

Loads and provides access to core business and operational principles 
from principles.yaml with dynamic variable interpolation and MCP JSON generation.

Intended for use by virtual agents (v_agents) and reporting tools.
"""

import yaml
import json
import logging
from datetime import datetime
from pathlib import Path
from string import Formatter
from typing import List, Dict, Any, Optional, Set

# --- Configuration ---
# Define paths relative to this file
PRINCIPLES_YAML_PATH = Path(__file__).parent / 'principles.yaml'
VERSION_LOG_PATH = Path(__file__).parent / 'version_log'

# Ensure version log directory exists
VERSION_LOG_PATH.mkdir(parents=True, exist_ok=True)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Private Cache ---
_PRINCIPLES_CACHE: Dict[str, Dict[str, Any]] = {}
_TEMPLATE_VARIABLES: Set[str] = set()

class MCPReport:
    """Handles MCP (Lightwave Media Control Protocol) report generation."""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.timestamp = datetime.now().isoformat()
        
    def to_json(self) -> Dict[str, Any]:
        """Convert the report to MCP JSON format."""
        return {
            "mcp_version": self.data.get("metadata", {}).get("mcp_version", "1.0"),
            "timestamp": self.timestamp,
            "type": "principles_report",
            "metadata": self.data.get("metadata", {}),
            "variables": self.data.get("variables", {}),
            "principles": self.data.get("principles", {}),
            "development_principles": self.data.get("development_principles", {}),
            "metrics": self._extract_metrics(),
            "status": self._calculate_status()
        }
        
    def _extract_metrics(self) -> Dict[str, Any]:
        """Extract all metrics from principles data."""
        metrics = {}
        for category in ["principles", "development_principles"]:
            for principle_key, principle in self.data.get(category, {}).items():
                for key, value in principle.items():
                    if any(metric in key for metric in ["metric", "score", "rate", "stats"]):
                        metrics[f"{principle_key}_{key}"] = value
        return metrics
        
    def _calculate_status(self) -> str:
        """Calculate overall status based on metrics."""
        # Placeholder: Implement actual status calculation logic
        return "healthy"

def extract_template_variables(yaml_content: str) -> Set[str]:
    """Extract all template variables from the YAML content."""
    variables = set()
    for match in Formatter().parse(yaml_content):
        if match[1] is not None:  # This is a variable
            variables.add(match[1])
    return variables

def load_principles_from_yaml(yaml_path: Path = PRINCIPLES_YAML_PATH) -> Dict[str, Dict[str, Any]]:
    """Loads principles from the specified YAML file."""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract template variables before parsing
            global _TEMPLATE_VARIABLES
            _TEMPLATE_VARIABLES = extract_template_variables(content)
            
            # Parse YAML content
            principles = yaml.safe_load(content)
            if not isinstance(principles, dict):
                logging.error(f"Error loading principles: YAML content is not a dictionary in {yaml_path}")
                return {}
            logging.info(f"Successfully loaded principles template with {len(_TEMPLATE_VARIABLES)} variables")
            return principles
    except FileNotFoundError:
        logging.error(f"Principles YAML file not found at: {yaml_path}")
        return {}
    except yaml.YAMLError as e:
        logging.error(f"Error parsing principles YAML file {yaml_path}: {e}")
        return {}
    except Exception as e:
        logging.error(f"An unexpected error occurred loading principles from {yaml_path}: {e}")
        return {}

def interpolate_variables(template_data: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
    """Interpolate variables in the template data."""
    def _interpolate(value: Any) -> Any:
        if isinstance(value, str):
            try:
                return value.format(**variables)
            except KeyError:
                return value  # Keep template if variable not provided
        elif isinstance(value, dict):
            return {k: _interpolate(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_interpolate(item) for item in value]
        return value

    return _interpolate(template_data)

def get_report_filename(variables: Dict[str, Any]) -> str:
    """Generate a clear, descriptive filename for the MCP report."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    env = variables.get('env', 'unknown')
    sprint = variables.get('active_sprint', 'no_sprint').replace('-', '_')
    version = variables.get('mcp_version', '1.0').replace('.', '_')
    
    return f"principles_report_v{version}_{env}_{sprint}_{timestamp}.json"

def generate_mcp_report(variables: Dict[str, Any], output_path: Optional[Path] = None) -> Dict[str, Any]:
    """Generate an MCP report with the current principles and provided variables."""
    if not _PRINCIPLES_CACHE:
        logging.warning("Principles cache empty when generating report. Reloading.")
        _initialize_principles()
    
    # Add default metadata if not provided
    variables.setdefault("current_timestamp", datetime.now().isoformat())
    variables.setdefault("company_name", "Lightwave Media LLC")
    variables.setdefault("env", "production")
    variables.setdefault("mcp_version", "1.0")
    variables.setdefault("user", "system")
    
    # Interpolate variables in the template
    interpolated_data = interpolate_variables(_PRINCIPLES_CACHE, variables)
    
    # Generate MCP report
    report = MCPReport(interpolated_data)
    mcp_json = report.to_json()
    
    # Save to file if path provided or use default version log path
    if output_path is None:
        filename = get_report_filename(variables)
        output_path = VERSION_LOG_PATH / filename
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(mcp_json, f, indent=2)
    logging.info(f"MCP report saved to {output_path}")
    
    return mcp_json

def get_template_variables() -> Set[str]:
    """Returns the set of template variables found in the YAML."""
    if not _TEMPLATE_VARIABLES:
        if not _PRINCIPLES_CACHE:
            _initialize_principles()
    return _TEMPLATE_VARIABLES.copy()

# --- Initialization ---
def _initialize_principles():
    """Initializes the principles cache by loading from YAML."""
    global _PRINCIPLES_CACHE
    _PRINCIPLES_CACHE = load_principles_from_yaml()

_initialize_principles() # Load principles when the module is imported

# --- Core Access Functions ---

def get_all_principles() -> Dict[str, Dict[str, Any]]:
    """Returns a copy of the entire dictionary of loaded principles."""
    if not _PRINCIPLES_CACHE:
        logging.warning("Attempted to get principles, but cache is empty. Reloading.")
        _initialize_principles()
    return _PRINCIPLES_CACHE.copy()

def get_principle(principle_key: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the details of a specific principle by its key from the cache.

    Args:
        principle_key: The unique key (e.g., "embrace_reality") for the principle.

    Returns:
        A dictionary containing the principle's details, or None if not found or not loaded.
    """
    if not _PRINCIPLES_CACHE:
         logging.warning(f"Principle cache empty when requesting key '{principle_key}'.")
         return None
    
    # Check both main principles and development principles
    principles = _PRINCIPLES_CACHE.get("principles", {})
    dev_principles = _PRINCIPLES_CACHE.get("development_principles", {})
    
    return principles.get(principle_key) or dev_principles.get(principle_key)

def find_principles_by_keyword(keyword: str) -> List[Dict[str, Any]]:
    """
    Finds principles from the cache that contain a specific keyword.

    Args:
        keyword: The keyword to search for (case-insensitive).

    Returns:
        A list of principle dictionaries matching the keyword.
    """
    if not _PRINCIPLES_CACHE:
        logging.warning(f"Principle cache empty when searching for keyword '{keyword}'.")
        return []

    keyword_lower = keyword.lower()
    matching_principles = []
    
    # Search in both main principles and development principles
    all_principles = {
        **_PRINCIPLES_CACHE.get("principles", {}),
        **_PRINCIPLES_CACHE.get("development_principles", {})
    }
    
    for principle in all_principles.values():
        # Check keywords list
        if keyword_lower in [kw.lower() for kw in principle.get("keywords", [])]:
            matching_principles.append(principle)
            continue
        # Check title
        if keyword_lower in principle.get("title", "").lower():
             matching_principles.append(principle)
             continue
        # Check description
        if keyword_lower in principle.get("description", "").lower():
             matching_principles.append(principle)

    # Remove potential duplicates
    unique_matches = []
    seen_ids = set()
    for p in matching_principles:
        p_id = p.get('id')
        if p_id not in seen_ids:
            unique_matches.append(p)
            seen_ids.add(p_id)

    return unique_matches

# --- Example Usage ---
if __name__ == "__main__":
    # Example: Generate an MCP report with some sample data
    sample_variables = {
        "current_timestamp": datetime.now().isoformat(),
        "company_name": "Lightwave Media LLC",
        "env": "development",
        "update_frequency": "daily",
        "mcp_version": "1.0",
        "user": "example_user",
        "review_cycle_days": "14",
        "company_quarterly_goals": "Improve code quality and test coverage",
        "active_sprint": "core-sprint-03",
        "current_team_focus": "API modernization",
        "current_key_metrics": "{'test_coverage': 85, 'api_response_time': 150}",
        "last_reality_check_date": datetime.now().isoformat(),
        "reality_alignment_score": "0.85",
        "recent_reality_examples": "Identified and addressed technical debt in auth system",
        # Add more variables as needed...
    }
    
    # Show available template variables
    print("\nTemplate Variables Found:")
    for var in get_template_variables():
        print(f"  - {var}")
    
    # Generate and save an MCP report with clear naming
    filename = get_report_filename(sample_variables)
    print(f"\nGenerating report with filename: {filename}")
    mcp_report = generate_mcp_report(sample_variables)  # Uses default version_log path
    
    print("\nReport Preview:")
    print(json.dumps(mcp_report, indent=2)[:500] + "...")  # Show first 500 chars
    
    # Example principle search
    print("\nPrinciples related to 'architecture':")
    arch_principles = find_principles_by_keyword("architecture")
    for p in arch_principles:
        print(f"  - {p['title']} (ID: {p['id']})")