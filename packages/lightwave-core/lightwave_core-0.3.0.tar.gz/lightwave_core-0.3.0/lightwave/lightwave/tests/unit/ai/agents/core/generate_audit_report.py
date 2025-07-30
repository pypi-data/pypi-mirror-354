#!/usr/bin/env python
# generate_audit_report.py - Script to generate audit reports from audit_agent.py

import os
import re
import json
import uuid
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_test_classes_and_methods(file_path: str):
    """Extract test classes and methods from a Python file using regex"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract class definitions with improved pattern
    class_pattern = r'class\s+(\w+)(?:\(.*?\))?\s*:'
    classes = re.findall(class_pattern, content)
    
    # Process each class to extract test methods
    result = {}
    for class_name in classes:
        # Skip if it doesn't look like a test class
        if not class_name.startswith('Test'):
            continue
            
        # Find class content
        class_pattern = r'class\s+' + re.escape(class_name) + r'(?:\(.*?\))?\s*:(.*?)(?=class\s+\w+\(|\Z)'
        class_match = re.search(class_pattern, content, re.DOTALL)
        if not class_match:
            continue
            
        class_content = class_match.group(1)
        
        # Try to extract class docstring
        docstring_pattern = r'"""(.*?)"""'
        docstring_match = re.search(docstring_pattern, class_content, re.DOTALL)
        class_doc = docstring_match.group(1).strip() if docstring_match else f"Tests for {class_name}"
        
        # Extract test methods
        method_pattern = r'def\s+(test_\w+)\s*\('
        method_names = re.findall(method_pattern, class_content)
        
        # Process methods
        methods = []
        for method_name in method_names:
            # Find method content
            method_pattern = r'def\s+' + re.escape(method_name) + r'\s*\(.*?\):(.*?)(?=\s+def\s+|\Z)'
            method_match = re.search(method_pattern, class_content, re.DOTALL)
            if not method_match:
                continue
                
            method_content = method_match.group(1)
            
            # Try to extract method docstring
            docstring_pattern = r'"""(.*?)"""'
            docstring_match = re.search(docstring_pattern, method_content, re.DOTALL)
            method_doc = docstring_match.group(1).strip() if docstring_match else f"Test method {method_name}"
            
            methods.append({
                "name": method_name,
                "description": method_doc,
                "status": "not_run"  # Since we're not actually running the tests
            })
        
        if methods:  # Only add classes that have test methods
            result[class_name] = {
                "description": class_doc,
                "tests": methods
            }
    
    return result

def generate_audit_results(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a simulated audit results structure"""
    # Create the basic structure
    results = {
        "summary": {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0
        },
        "categories": test_data,
        "metadata": {
            "audit_id": str(uuid.uuid4()),
            "audit_type": "agent_audit",
            "target": "LightWave AI Services",
            "component": "Agent Core",
            "version": "1.0.0",
            "created_by": os.environ.get("USER", "automated"),
            "environment": os.environ.get("ENV", "development")
        }
    }
    
    # Count the total number of tests
    total_tests = 0
    for category, data in test_data.items():
        total_tests += len(data["tests"])
    
    results["summary"]["total_tests"] = total_tests
    results["summary"]["skipped"] = total_tests  # Mark all as skipped since we're not running them
    
    return results

def generate_markdown_report(results: Dict[str, Any], output_file: str):
    """Generate a Markdown report from the test results"""
    with open(output_file, 'w') as f:
        # Write header
        f.write("# Agent Audit Report\n\n")
        f.write(f"Generated on: {results['summary']['timestamp']}\n")
        f.write(f"Audit ID: {results['metadata']['audit_id']}\n")
        f.write(f"Target: {results['metadata']['target']} - {results['metadata']['component']}\n")
        f.write(f"Environment: {results['metadata']['environment']}\n\n")
        
        # Write summary
        f.write("## Summary\n\n")
        f.write(f"- **Total Tests**: {results['summary']['total_tests']}\n")
        f.write(f"- **Tests Available**: {results['summary']['total_tests']}\n")
        f.write("- **Note**: This is a static analysis of the audit test suite without executing the tests.\n\n")
        
        # Create table of contents
        f.write("## Table of Contents\n\n")
        for category, data in results["categories"].items():
            test_count = len(data["tests"])
            f.write(f"- [{category}](#{category.lower()}) ({test_count} tests)\n")
        f.write("- [Additional Recommendations](#additional-recommendations)\n\n")
        
        # Write categories and tests
        for category, data in results["categories"].items():
            test_count = len(data["tests"])
            f.write(f"## {category}\n\n")
            f.write(f"{data['description']}\n\n")
            f.write(f"**Tests in this category: {test_count}**\n\n")
            
            # Group tests by status
            grouped_tests = {"not_run": []}
            for test in data["tests"]:
                status = test["status"]
                if status not in grouped_tests:
                    grouped_tests[status] = []
                grouped_tests[status].append(test)
            
            # Write tests grouped by status
            for status, tests in grouped_tests.items():
                if not tests:
                    continue
                    
                status_label = "Not Run" if status == "not_run" else status.capitalize()
                if status == "not_run":
                    status_icon = "⏭️"
                elif status == "passed":
                    status_icon = "✅"
                elif status == "failed":
                    status_icon = "❌"
                elif status == "skipped":
                    status_icon = "⏩"
                else:
                    status_icon = "❓"
                
                if len(tests) > 0:
                    f.write(f"### {status_icon} {status_label} Tests ({len(tests)})\n\n")
                    
                    for test in tests:
                        f.write(f"#### {test['name']}\n\n")
                        f.write(f"{test['description']}\n\n")
                        
                        if test.get("error"):
                            f.write("**Error:**\n\n")
                            f.write("```\n")
                            f.write(test["error"])
                            f.write("\n```\n\n")
        
        # Write recommendations section
        f.write("## Additional Recommendations\n\n")
        f.write("The following recommendations are based on best practices identified in the audit code:\n\n")
        
        if "recommendations" in results and results["recommendations"]:
            for rec in results["recommendations"]:
                f.write(f"- **{rec['title']}**: {rec['description']}\n")
        else:
            f.write("- **Code Review:** Perform manual code reviews focusing on logic, clarity, security, and adherence to LangGraph/Pydantic AI patterns.\n")
            f.write("- **Static Analysis:** Use tools like `mypy` for type checking and `flake8` or `ruff` for linting.\n")
            f.write("- **Test Coverage:** Integrate `pytest-cov` to measure test coverage and identify untested code paths.\n")
            f.write("- **Dependency Management:** Ensure `requirements.txt` is accurate and minimal. Audit third-party library licenses if necessary.\n")
            f.write("- **Logging & Monitoring:** Ensure logging provides sufficient detail for debugging production issues. Integrate with monitoring tools (like LangSmith).\n")

def extract_additional_recommendations(file_path: str):
    """Extract additional recommendations from the comments at the end of the file"""
    recommendations = []
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for recommendations section at the end
    recommendations_pattern = r'# --- Further Audit Recommendations.*?$(.*?)(?:\Z|^#)'
    match = re.search(recommendations_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        rec_text = match.group(1).strip()
        # Extract individual recommendations
        rec_lines = re.findall(r'# - \*\*(.*?)\*\*(.*?)(?=$|# -)', rec_text, re.MULTILINE | re.DOTALL)
        
        for title, desc in rec_lines:
            recommendations.append({
                "title": title.strip(),
                "description": desc.strip()
            })
    
    return recommendations

def generate_filename_prefix(results: Dict[str, Any]) -> str:
    """Generate a meaningful filename prefix based on audit metadata"""
    component = results["metadata"]["component"].lower().replace(" ", "_")
    env = results["metadata"]["environment"]
    audit_type = results["metadata"]["audit_type"]
    audit_id = results["metadata"]["audit_id"][:8]  # Use first 8 chars of UUID
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    return f"audit_{component}_{audit_type}_{env}_{timestamp}_{audit_id}"

def main():
    """Main function to generate audit reports"""
    parser = argparse.ArgumentParser(description="Generate audit reports")
    parser.add_argument("--component", default="Agent Core", help="Component being audited")
    parser.add_argument("--env", default=os.environ.get("ENV", "development"), help="Environment (development, staging, production)")
    parser.add_argument("--output-dir", default="reports", help="Directory to save reports")
    args = parser.parse_args()
    
    # Define the file to analyze - use absolute path
    audit_file = os.path.join(os.path.dirname(__file__), "audit_agent.py")
    
    # Create reports directory if it doesn't exist
    reports_dir = Path(args.output_dir)
    reports_dir.mkdir(exist_ok=True)
    
    # Extract test data
    print(f"Analyzing {audit_file}...")
    test_data = extract_test_classes_and_methods(audit_file)
    
    # Extract additional recommendations
    recommendations = extract_additional_recommendations(audit_file)
    
    # Generate results
    results = generate_audit_results(test_data)
    
    # Update metadata with command line args
    results["metadata"]["component"] = args.component
    results["metadata"]["environment"] = args.env
    
    # Add recommendations to results
    results["recommendations"] = recommendations
    
    # Generate filename prefix
    filename_prefix = generate_filename_prefix(results)
    
    # Generate reports
    md_file = reports_dir / f"{filename_prefix}.md"
    json_file = reports_dir / f"{filename_prefix}.json"
    
    print(f"Generating Markdown report: {md_file}")
    generate_markdown_report(results, md_file)
    
    print(f"Generating JSON report: {json_file}")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Audit report generation complete.")
    print(f"Markdown report: {md_file}")
    print(f"JSON report: {json_file}")
    
    # Return the generated filenames for use by other scripts
    return md_file, json_file

if __name__ == "__main__":
    main() 