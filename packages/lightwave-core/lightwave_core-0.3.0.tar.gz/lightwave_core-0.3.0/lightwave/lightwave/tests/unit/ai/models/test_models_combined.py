#!/usr/bin/env python3
"""
Combined model tests for the Lightwave AI Services.
This file includes tests for model validation, conflict detection, and direct model usage.
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the src directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class TestModels:
    def test_no_naming_conflicts(self):
        """Test that there are no naming conflicts in the models."""
        from src.agents.core.test_documentation import (
            TestDocumentationSystem,
            TestSuite,
            TestResult,
            TestReport,
            TestArtifact
        )
        
        from src.agents.core.certification_report import (
            CertificationReportGenerator,
            CertificationCriteria,
            CertificationResult,
            CertificationReport
        )
        
        # If we get here without any import errors, there are no naming conflicts
        print("✅ No naming conflicts detected!")
        assert True
    
    def test_model_direct_usage(self):
        """Test direct usage of the models."""
        # Import models
        from src.agents.core.test_documentation import (
            TestSuite,
            TestResult,
            TestReport,
            TestArtifact
        )
        
        # Create test models directly
        test_result = TestResult(
            test_id="test-1",
            test_name="Example Test",
            result="pass",
            duration=0.5,
            timestamp=datetime.now(),
            error_message=None,
            metadata={"key": "value"}
        )
        
        test_suite = TestSuite(
            suite_id="suite-1",
            name="Example Suite",
            description="A test suite",
            test_results=[test_result],
            timestamp=datetime.now()
        )
        
        assert test_result.test_name == "Example Test"
        assert test_result.result == "pass"
        assert test_suite.name == "Example Suite"
        assert len(test_suite.test_results) == 1
        
        # Create a report with the suite
        report = TestReport(
            report_id="report-1",
            title="Test Report",
            generated_by="Test Script",
            description="Example report",
            timestamp=datetime.now(),
            suites=[test_suite]
        )
        
        assert report.title == "Test Report"
        assert len(report.suites) == 1
        
        print("✅ Direct model usage passed!")
        assert True
    
    def test_minimal_model_usage(self):
        """Test minimal model usage with validation."""
        from datetime import datetime
        from src.agents.core.test_documentation import (
            TestSuite,
            TestResult
        )
        
        # Create minimal test objects with required fields
        result = TestResult(
            test_id="minimal-1",
            test_name="Minimal Test",
            result="pass",
            timestamp=datetime.now(),
            duration=0.1  # Adding the required duration field
        )
        
        suite = TestSuite(
            suite_id="minimal-suite-1",
            name="Minimal Suite",
            timestamp=datetime.now()
        )
        
        # Validate fields are populated correctly
        assert result.test_id == "minimal-1"
        assert result.test_name == "Minimal Test"
        assert result.result == "pass"
        assert isinstance(result.timestamp, datetime)
        assert result.duration == 0.1
        
        assert suite.suite_id == "minimal-suite-1"
        assert suite.name == "Minimal Suite"
        assert suite.test_results == []
        
        print("✅ Minimal model validation passed!")
        assert True

if __name__ == "__main__":
    test = TestModels()
    test.test_no_naming_conflicts()
    test.test_model_direct_usage()
    test.test_minimal_model_usage()
    print("All model tests passed successfully!") 