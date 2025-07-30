#!/usr/bin/env python
# run_audit.py - Script to run audit tests and generate reports

import os
import json
import pytest
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import importlib.util

# Function to load a Python module by file path
def load_module_from_path(file_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load the audit_agent module to get test classes
audit_module = load_module_from_path("audit_agent.py", "audit_agent")

# Define a custom pytest reporter that captures results
class AuditReporter:
    def __init__(self):
        self.results = {
            "summary": {
                "timestamp": datetime.datetime.now().isoformat(),
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": 0
            },
            "categories": {}
        }
        
    def pytest_runtest_logreport(self, report):
        if report.when != "call" and not (report.when == "setup" and report.skipped):
            return
            
        # Extract test category and name
        nodeid = report.nodeid
        parts = nodeid.split("::")
        if len(parts) >= 3:
            test_file = parts[0]
            test_class = parts[1]
            test_name = parts[2]
            
            # Create category if it doesn't exist
            if test_class not in self.results["categories"]:
                # Get the class docstring if available
                cls_obj = getattr(audit_module, test_class, None)
                description = cls_obj.__doc__ if cls_obj and cls_obj.__doc__ else f"Tests for {test_class}"
                
                self.results["categories"][test_class] = {
                    "description": description,
                    "tests": []
                }
            
            # Determine test result
            status = "passed"
            if report.skipped:
                status = "skipped"
                self.results["summary"]["skipped"] += 1
            elif report.failed:
                if report.longrepr and "XFAIL" in str(report.longrepr):
                    status = "xfailed"
                elif report.longrepr and "XPASS" in str(report.longrepr):
                    status = "xpassed"
                else:
                    status = "failed"
                    self.results["summary"]["failed"] += 1
            else:
                self.results["summary"]["passed"] += 1
            
            # Extract docstring and message
            test_func = None
            for cls_name, cls_obj in vars(audit_module).items():
                if cls_name == test_class and hasattr(cls_obj, test_name):
                    test_func = getattr(cls_obj, test_name)
                    break
            
            docstring = test_func.__doc__ if test_func and test_func.__doc__ else f"Test {test_name}"
            error_message = str(report.longrepr) if report.failed and report.longrepr else None
            
            # Add test result
            self.results["categories"][test_class]["tests"].append({
                "name": test_name,
                "description": docstring,
                "status": status,
                "error": error_message
            })
            
            self.results["summary"]["total_tests"] += 1
            
    def get_results(self):
        return self.results

def run_audit_tests():
    # Create a pytest session with our custom reporter
    reporter = AuditReporter()
    pytest.main(["audit_agent.py", "-v"], plugins=[reporter])
    return reporter.get_results()

def generate_markdown_report(results: Dict[str, Any], output_file: str):
    """Generate a Markdown report from the test results"""
    with open(output_file, 'w') as f:
        # Write header
        f.write("# Agent Audit Report\n\n")
        f.write(f"Generated on: {results['summary']['timestamp']}\n\n")
        
        # Write summary
        f.write("## Summary\n\n")
        f.write(f"- **Total Tests**: {results['summary']['total_tests']}\n")
        f.write(f"- **Passed**: {results['summary']['passed']}\n")
        f.write(f"- **Failed**: {results['summary']['failed']}\n")
        f.write(f"- **Skipped**: {results['summary']['skipped']}\n\n")
        
        # Write categories and tests
        for category, data in results["categories"].items():
            f.write(f"## {category}\n\n")
            f.write(f"{data['description']}\n\n")
            
            for test in data["tests"]:
                status_icon = "✅" if test["status"] == "passed" else "❌" if test["status"] == "failed" else "⏭️"
                f.write(f"### {status_icon} {test['name']}\n\n")
                f.write(f"{test['description']}\n\n")
                
                if test["error"]:
                    f.write("**Error:**\n\n")
                    f.write("```\n")
                    f.write(test["error"])
                    f.write("\n```\n\n")
        
        # Write recommendations
        f.write("## Additional Recommendations\n\n")
        f.write("The following recommendations are based on best practices and cannot be fully automated:\n\n")
        f.write("- **Code Review:** Perform manual code reviews focusing on logic, clarity, security, and adherence to LangGraph/Pydantic AI patterns.\n")
        f.write("- **Static Analysis:** Use tools like `mypy` for type checking and `flake8` or `ruff` for linting.\n")
        f.write("- **Test Coverage:** Integrate `pytest-cov` to measure test coverage and identify untested code paths.\n")
        f.write("- **Dependency Management:** Ensure `requirements.txt` is accurate and minimal. Audit third-party library licenses if necessary.\n")
        f.write("- **Logging & Monitoring:** Ensure logging provides sufficient detail for debugging production issues. Integrate with monitoring tools (like LangSmith).\n")

def main():
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Run tests and get results
    print("Running audit tests...")
    results = run_audit_tests()
    
    # Generate reports
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = reports_dir / f"audit_report_{timestamp}.md"
    json_file = reports_dir / f"audit_report_{timestamp}.json"
    
    print(f"Generating Markdown report: {md_file}")
    generate_markdown_report(results, md_file)
    
    print(f"Generating JSON report: {json_file}")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Audit complete. Reports generated.")
    print(f"Markdown report: {md_file}")
    print(f"JSON report: {json_file}")

if __name__ == "__main__":
    main() 