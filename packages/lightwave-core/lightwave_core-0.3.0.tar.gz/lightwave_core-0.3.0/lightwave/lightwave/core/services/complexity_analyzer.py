from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import math
from dataclasses import dataclass
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from pydantic import BaseModel, Field

from ..models.task import Task, TaskStatus, TaskPriority
from ..models.dependency_graph import DependencyGraph
from .ml_complexity_predictor import MLComplexityPredictor
from .task_history_analyzer import TaskHistoryAnalyzer

class ComplexityLevel(str):
    """Complexity level classification."""
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

class TimeEstimate(BaseModel):
    """Time estimate for a task."""
    optimistic: int  # hours
    likely: int     # hours
    pessimistic: int  # hours
    
    @property
    def pert_estimate(self) -> float:
        """Calculate PERT estimate: (O + 4L + P) / 6."""
        return (self.optimistic + 4 * self.likely + self.pessimistic) / 6
    
    @property
    def standard_deviation(self) -> float:
        """Calculate standard deviation: (P - O) / 6."""
        return (self.pessimistic - self.optimistic) / 6

@dataclass
class ComplexityMetrics:
    """Holds complexity metrics for a task."""
    dependency_complexity: float
    structural_complexity: float
    implementation_complexity: float
    testing_complexity: float
    risk_factors: List[Dict[str, Any]]
    ml_predicted_complexity: Optional[float] = None
    ml_confidence: Optional[float] = None
    historical_metrics: Optional[Dict[str, Any]] = None

class ComplexityReport(BaseModel):
    """Enhanced task complexity analysis report."""
    meta: Dict[str, Any]
    complexity_analysis: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    time_estimates: Dict[str, TimeEstimate]
    recommendations: List[str]

@dataclass
class ComplexityScore:
    """Represents a task's complexity score and contributing factors."""
    score: float
    factors: Dict[str, float]
    confidence: float

class ComplexityAnalyzer:
    """Analyzes task complexity using various metrics and ML models."""
    
    COMPLEXITY_LEVELS = {
        'LOW': (0, 3),
        'MEDIUM': (3, 7),
        'HIGH': (7, float('inf'))
    }
    
    def __init__(self, dependency_graph: DependencyGraph):
        self.dependency_graph = dependency_graph
        self.ml_predictor = MLComplexityPredictor()
        self.history_analyzer = TaskHistoryAnalyzer()
        self._complexity_thresholds = {
            ComplexityLevel.TRIVIAL: 2.0,
            ComplexityLevel.SIMPLE: 4.0,
            ComplexityLevel.MODERATE: 6.0,
            ComplexityLevel.COMPLEX: 8.0,
            ComplexityLevel.VERY_COMPLEX: 10.0
        }
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    
    def analyze_task(self, task: Task) -> ComplexityScore:
        """Analyze a task's complexity."""
        # Extract features
        features = self._extract_features(task)
        
        # Get ML prediction
        ml_score = self.ml_predictor.predict(features)
        
        # Calculate heuristic score
        heuristic_score = self._calculate_heuristic_score(task)
        
        # Combine scores with weights
        final_score = 0.7 * ml_score + 0.3 * heuristic_score
        
        # Calculate confidence based on feature completeness
        confidence = self._calculate_confidence(features)
        
        # Get contributing factors
        factors = self._identify_complexity_factors(task)
        
        return ComplexityScore(
            score=final_score,
            factors=factors,
            confidence=confidence
        )
    
    def _extract_features(self, task: Task) -> Dict[str, float]:
        """Extract numerical features from a task for ML prediction."""
        return {
            'description_length': len(task.description),
            'num_dependencies': len(task.dependencies),
            'num_subtasks': len(task.subtasks) if task.subtasks else 0,
            'priority_value': self._priority_to_value(task.priority),
            'has_test_strategy': 1.0 if task.test_strategy else 0.0,
            'has_implementation_details': 1.0 if task.details else 0.0
        }
    
    def _calculate_heuristic_score(self, task: Task) -> float:
        """Calculate complexity score based on heuristic rules."""
        score = 0.0
        
        # Base score from priority
        priority_scores = {'low': 1.0, 'medium': 2.0, 'high': 3.0, 'critical': 4.0}
        score += priority_scores.get(task.priority, 2.0)
        
        # Add points for dependencies
        score += len(task.dependencies) * 0.5
        
        # Add points for subtasks
        if task.subtasks:
            score += len(task.subtasks) * 0.3
        
        # Add points for long descriptions (indicating complexity)
        score += min(len(task.description) / 500, 2.0)
        
        # Normalize to 0-10 scale
        return min(score / 10.0 * 10, 10.0)
    
    def _calculate_confidence(self, features: Dict[str, float]) -> float:
        """Calculate confidence in the complexity score based on available information."""
        # Count how many features have meaningful values
        total_features = len(features)
        valid_features = sum(1 for v in features.values() if v > 0)
        
        return valid_features / total_features
    
    def _identify_complexity_factors(self, task: Task) -> Dict[str, float]:
        """Identify factors contributing to task complexity."""
        factors = {}
        
        # Dependencies
        if task.dependencies:
            factors['dependencies'] = len(task.dependencies) * 0.5
        
        # Subtasks
        if task.subtasks:
            factors['subtasks'] = len(task.subtasks) * 0.3
        
        # Description length
        desc_score = min(len(task.description) / 500, 2.0)
        if desc_score > 1.0:
            factors['description_complexity'] = desc_score
        
        # Priority
        priority_scores = {'low': 1.0, 'medium': 2.0, 'high': 3.0, 'critical': 4.0}
        factors['priority'] = priority_scores.get(task.priority, 2.0)
        
        return factors
    
    def _priority_to_value(self, priority: str) -> float:
        """Convert priority string to numerical value."""
        priority_values = {
            'low': 1.0,
            'medium': 2.0,
            'high': 3.0,
            'critical': 4.0
        }
        return priority_values.get(priority, 2.0)
    
    def _calculate_base_metrics(self, task: Task) -> ComplexityMetrics:
        """Calculate base complexity metrics for a task."""
        # Dependency complexity
        dep_complexity = min(10.0, len(task.dependencies) * 1.5)
        
        # Structural complexity based on subtasks and their relationships
        structural_complexity = self._calculate_structural_complexity(task)
        
        # Implementation complexity based on task description and requirements
        impl_complexity = self._analyze_implementation_complexity(task)
        
        # Testing complexity
        testing_complexity = self._estimate_testing_complexity(task)
        
        # Risk factors
        risk_factors = self._identify_risk_factors(task)
        
        return ComplexityMetrics(
            dependency_complexity=dep_complexity,
            structural_complexity=structural_complexity,
            implementation_complexity=impl_complexity,
            testing_complexity=testing_complexity,
            risk_factors=risk_factors
        )
    
    def _calculate_structural_complexity(self, task: Task) -> float:
        """Calculate structural complexity based on task structure."""
        base_complexity = len(task.subtasks) * 1.2
        
        # Add complexity for nested subtasks
        nested_depth = self._calculate_subtask_depth(task)
        depth_factor = 1.0 + (nested_depth * 0.5)
        
        # Add complexity for dependencies between subtasks
        subtask_deps = self._count_subtask_dependencies(task)
        dep_factor = 1.0 + (subtask_deps * 0.3)
        
        return min(10.0, base_complexity * depth_factor * dep_factor)
    
    def _calculate_subtask_depth(self, task: Task) -> int:
        """Calculate maximum depth of nested subtasks."""
        max_depth = 0
        for subtask in task.subtasks:
            depth = 1 + self._calculate_subtask_depth(subtask)
            max_depth = max(max_depth, depth)
        return max_depth
    
    def _count_subtask_dependencies(self, task: Task) -> int:
        """Count dependencies between subtasks."""
        count = 0
        for subtask in task.subtasks:
            count += len([
                dep for dep in subtask.dependencies
                if any(dep == st.id for st in task.subtasks)
            ])
        return count
    
    def _analyze_implementation_complexity(self, task: Task) -> float:
        """Analyze implementation complexity based on task details."""
        complexity = 5.0  # Base complexity
        
        # Adjust based on task description keywords
        desc = (task.description or "").lower()
        
        # Technical complexity indicators
        tech_keywords = {
            'high': ['algorithm', 'optimization', 'scalability', 'performance'],
            'medium': ['integration', 'api', 'database', 'async'],
            'low': ['ui', 'styling', 'text', 'documentation']
        }
        
        for level, keywords in tech_keywords.items():
            matches = sum(1 for kw in keywords if kw in desc)
            if level == 'high':
                complexity += matches * 1.5
            elif level == 'medium':
                complexity += matches * 1.0
            else:
                complexity += matches * 0.5
        
        return min(10.0, complexity)
    
    def _estimate_testing_complexity(self, task: Task) -> float:
        """Estimate testing complexity for the task."""
        complexity = 3.0  # Base testing complexity
        
        desc = (task.description or "").lower()
        
        # Testing complexity indicators
        test_factors = {
            'unit tests': 1.0,
            'integration tests': 2.0,
            'e2e tests': 2.5,
            'performance tests': 2.0,
            'security tests': 2.0
        }
        
        for factor, weight in test_factors.items():
            if factor in desc:
                complexity += weight
        
        # Additional complexity for tasks with dependencies
        complexity += len(task.dependencies) * 0.5
        
        return min(10.0, complexity)
    
    def _identify_risk_factors(self, task: Task) -> List[Dict[str, Any]]:
        """Identify potential risk factors for the task."""
        risks = []
        
        # Dependency risks
        if len(task.dependencies) > 3:
            risks.append({
                'type': 'dependency_overload',
                'severity': 'high',
                'description': 'Task has many dependencies, increasing coordination complexity'
            })
        
        # Structural risks
        if len(task.subtasks) > 5:
            risks.append({
                'type': 'high_subtask_count',
                'severity': 'medium',
                'description': 'Large number of subtasks may indicate scope creep'
            })
        
        # Historical risks
        if (
            task.historical_metrics and
            task.historical_metrics.get('estimate_accuracy', {}).get('time_estimate_accuracy', 1.0) < 0.7
        ):
            risks.append({
                'type': 'historical_estimate_inaccuracy',
                'severity': 'medium',
                'description': 'Similar tasks have had poor estimate accuracy'
            })
        
        return risks
    
    def _calculate_overall_complexity(self, metrics: ComplexityMetrics) -> str:
        """Calculate overall complexity level using all available data."""
        # Base complexity score from traditional metrics
        base_score = (
            metrics.dependency_complexity * 0.25 +
            metrics.structural_complexity * 0.25 +
            metrics.implementation_complexity * 0.3 +
            metrics.testing_complexity * 0.2
        )
        
        # Adjust score using ML predictions if available
        if metrics.ml_predicted_complexity is not None:
            confidence_weight = metrics.ml_confidence or 0.5
            base_score = (
                base_score * (1 - confidence_weight) +
                metrics.ml_predicted_complexity * confidence_weight
            )
        
        # Adjust using historical data if available
        if metrics.historical_metrics:
            historical_complexity = metrics.historical_metrics.get(
                'estimate_accuracy', {}
            ).get('complexity_estimate_accuracy', 0.0) * 10.0
            base_score = (base_score * 0.7 + historical_complexity * 0.3)
        
        # Determine complexity level
        for level, (min_val, max_val) in self.COMPLEXITY_LEVELS.items():
            if min_val <= base_score < max_val:
                return level
        
        return 'HIGH'  # Default to high if something goes wrong
    
    def _estimate_time(self, metrics: ComplexityMetrics, task: Task) -> Dict[str, Any]:
        """Estimate time required for task completion."""
        # Base time estimate using PERT technique
        optimistic = self._calculate_optimistic_time(metrics)
        pessimistic = self._calculate_pessimistic_time(metrics)
        most_likely = self._calculate_most_likely_time(metrics)
        
        # PERT estimate
        pert_estimate = (optimistic + (4 * most_likely) + pessimistic) / 6
        
        # Adjust using ML predictions if available
        if metrics.ml_predicted_complexity is not None:
            ml_time_factor = metrics.ml_predicted_complexity / 5.0  # Normalize to 0-2 range
            pert_estimate *= ml_time_factor
        
        # Adjust using historical data if available
        if metrics.historical_metrics:
            hist_avg_time = metrics.historical_metrics.get('avg_completion_time')
            if hist_avg_time:
                # Blend PERT estimate with historical average
                pert_estimate = (pert_estimate * 0.7 + hist_avg_time.total_seconds() / 3600 * 0.3)
        
        return {
            'optimistic': timedelta(hours=optimistic),
            'pessimistic': timedelta(hours=pessimistic),
            'most_likely': timedelta(hours=most_likely),
            'expected': timedelta(hours=pert_estimate),
            'confidence': self._calculate_estimate_confidence(metrics)
        }
    
    def _calculate_optimistic_time(self, metrics: ComplexityMetrics) -> float:
        """Calculate optimistic time estimate in hours."""
        return max(1.0, (
            metrics.dependency_complexity * 0.5 +
            metrics.structural_complexity * 0.5 +
            metrics.implementation_complexity * 1.0 +
            metrics.testing_complexity * 0.5
        ))
    
    def _calculate_pessimistic_time(self, metrics: ComplexityMetrics) -> float:
        """Calculate pessimistic time estimate in hours."""
        return max(4.0, (
            metrics.dependency_complexity * 2.0 +
            metrics.structural_complexity * 2.0 +
            metrics.implementation_complexity * 3.0 +
            metrics.testing_complexity * 2.0
        ))
    
    def _calculate_most_likely_time(self, metrics: ComplexityMetrics) -> float:
        """Calculate most likely time estimate in hours."""
        return max(2.0, (
            metrics.dependency_complexity * 1.0 +
            metrics.structural_complexity * 1.0 +
            metrics.implementation_complexity * 1.5 +
            metrics.testing_complexity * 1.0
        ))
    
    def _calculate_estimate_confidence(self, metrics: ComplexityMetrics) -> float:
        """Calculate confidence level in time estimate."""
        confidence = 0.8  # Base confidence
        
        # Reduce confidence based on risk factors
        confidence -= len(metrics.risk_factors) * 0.1
        
        # Adjust based on ML confidence if available
        if metrics.ml_confidence is not None:
            confidence = (confidence + metrics.ml_confidence) / 2
        
        # Adjust based on historical data
        if metrics.historical_metrics:
            historical_accuracy = metrics.historical_metrics.get(
                'estimate_accuracy', {}
            ).get('time_estimate_accuracy', 0.0)
            confidence = (confidence + historical_accuracy) / 2
        
        return max(0.1, min(1.0, confidence))
    
    def _assess_risks(self, metrics: ComplexityMetrics, task: Task) -> Dict[str, Any]:
        """Assess risks and provide mitigation strategies."""
        risks = metrics.risk_factors.copy()
        
        # Add ML-based risks if available
        if metrics.ml_predicted_complexity is not None:
            if metrics.ml_predicted_complexity > 7.0:
                risks.append({
                    'type': 'ml_predicted_high_complexity',
                    'severity': 'high',
                    'description': 'ML model predicts high complexity'
                })
        
        # Add historical risks
        if metrics.historical_metrics:
            patterns = metrics.historical_metrics.get('patterns', [])
            for pattern in patterns:
                if pattern['pattern_type'] == 'common_blockers':
                    risks.append({
                        'type': 'historical_blockers',
                        'severity': 'medium',
                        'description': 'Similar tasks often face specific blockers',
                        'details': pattern['details']
                    })
        
        return {
            'identified_risks': risks,
            'overall_risk_level': self._calculate_risk_level(risks),
            'mitigation_strategies': self._generate_mitigation_strategies(risks)
        }
    
    def _calculate_risk_level(self, risks: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level."""
        severity_scores = {
            'low': 1,
            'medium': 2,
            'high': 3
        }
        
        total_score = sum(
            severity_scores[risk['severity']]
            for risk in risks
        )
        
        if total_score <= 2:
            return 'LOW'
        elif total_score <= 5:
            return 'MEDIUM'
        else:
            return 'HIGH'
    
    def _generate_mitigation_strategies(self, risks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate mitigation strategies for identified risks."""
        strategies = []
        
        for risk in risks:
            if risk['type'] == 'dependency_overload':
                strategies.append({
                    'risk_type': risk['type'],
                    'strategy': 'Break down dependencies into smaller, more manageable chunks'
                })
            elif risk['type'] == 'high_subtask_count':
                strategies.append({
                    'risk_type': risk['type'],
                    'strategy': 'Review subtasks for potential consolidation or parallelization'
                })
            elif risk['type'] == 'historical_estimate_inaccuracy':
                strategies.append({
                    'risk_type': risk['type'],
                    'strategy': 'Add buffer time and increase monitoring frequency'
                })
            elif risk['type'] == 'ml_predicted_high_complexity':
                strategies.append({
                    'risk_type': risk['type'],
                    'strategy': 'Consider breaking down the task or allocating additional resources'
                })
            elif risk['type'] == 'historical_blockers':
                strategies.append({
                    'risk_type': risk['type'],
                    'strategy': 'Proactively address common blockers identified from similar tasks'
                })
        
        return strategies
    
    def _generate_recommendations(self, metrics: ComplexityMetrics, task: Task) -> List[str]:
        """Generate recommendations for task execution."""
        recommendations = []
        
        # Complexity-based recommendations
        if metrics.dependency_complexity > 7.0:
            recommendations.append(
                "Consider breaking down dependencies or implementing them incrementally"
            )
        
        if metrics.structural_complexity > 7.0:
            recommendations.append(
                "Review task structure for potential simplification"
            )
        
        # ML-based recommendations
        if metrics.ml_predicted_complexity is not None:
            if metrics.ml_predicted_complexity > 7.0:
                recommendations.append(
                    "Based on ML analysis, consider allocating additional resources"
                )
        
        # Historical data-based recommendations
        if metrics.historical_metrics:
            patterns = metrics.historical_metrics.get('patterns', [])
            for pattern in patterns:
                if pattern['pattern_type'] == 'status_transitions':
                    recommendations.append(
                        "Based on historical patterns, plan for potential status transitions"
                    )
        
        return recommendations
    
    def _format_metrics(self, metrics: ComplexityMetrics) -> Dict[str, Any]:
        """Format complexity metrics for output."""
        formatted = {
            'dependency_complexity': metrics.dependency_complexity,
            'structural_complexity': metrics.structural_complexity,
            'implementation_complexity': metrics.implementation_complexity,
            'testing_complexity': metrics.testing_complexity,
            'risk_factors': metrics.risk_factors
        }
        
        if metrics.ml_predicted_complexity is not None:
            formatted.update({
                'ml_predicted_complexity': metrics.ml_predicted_complexity,
                'ml_confidence': metrics.ml_confidence
            })
        
        if metrics.historical_metrics:
            formatted['historical_metrics'] = metrics.historical_metrics
        
        return formatted
    
    def analyze_all_tasks(self, threshold_score: float = 5.0) -> ComplexityReport:
        """Generate a comprehensive complexity report for all tasks."""
        analysis = []
        time_estimates = {}
        all_risks = []
        
        for task in self.dependency_graph.tasks.values():
            task_analysis = self.analyze_task(task)
            analysis.append(task_analysis)
            time_estimates[str(task.id)] = TimeEstimate(**task_analysis["timeEstimate"])
            all_risks.append(task_analysis["riskAssessment"])
        
        # Sort by complexity (highest first)
        analysis.sort(key=lambda x: x["score"], reverse=True)
        
        # Generate project-level risk assessment
        risk_assessment = self._aggregate_risk_assessment(all_risks)
        
        # Generate recommendations
        recommendations = self._generate_project_recommendations(analysis)
        
        meta = {
            "generatedAt": datetime.utcnow().isoformat(),
            "tasksAnalyzed": len(analysis),
            "thresholdScore": threshold_score,
            "projectName": "lightwave-cli",
            "totalTimeEstimate": self._aggregate_time_estimates(time_estimates),
            "overallRiskLevel": risk_assessment["overallRiskLevel"]
        }
        
        return ComplexityReport(
            meta=meta,
            complexity_analysis=analysis,
            risk_assessment=risk_assessment,
            time_estimates=time_estimates,
            recommendations=recommendations
        )
    
    def _aggregate_risk_assessment(self, task_risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate individual task risks into project-level assessment."""
        risk_levels = [r["riskLevel"] for r in task_risks]
        risk_factors = [factor for r in task_risks for factor in r["riskFactors"]]
        
        # Calculate overall risk level
        high_risks = risk_levels.count("high")
        medium_risks = risk_levels.count("medium")
        
        if high_risks > len(task_risks) * 0.2:  # More than 20% high risk
            overall_level = "high"
        elif high_risks > 0 or medium_risks > len(task_risks) * 0.3:
            overall_level = "medium"
        else:
            overall_level = "low"
        
        return {
            "overallRiskLevel": overall_level,
            "highRiskCount": high_risks,
            "mediumRiskCount": medium_risks,
            "lowRiskCount": risk_levels.count("low"),
            "commonRiskFactors": self._identify_common_risks(risk_factors),
            "mitigationStrategies": self._generate_project_mitigations(overall_level, risk_factors)
        }
    
    def _identify_common_risks(self, risk_factors: List[str], threshold: int = 2) -> List[str]:
        """Identify commonly occurring risk factors."""
        from collections import Counter
        risk_counts = Counter(risk_factors)
        return [risk for risk, count in risk_counts.items() if count >= threshold]
    
    def _aggregate_time_estimates(self, estimates: Dict[str, TimeEstimate]) -> Dict[str, Any]:
        """Aggregate individual time estimates into project-level estimate."""
        total_optimistic = sum(e.optimistic for e in estimates.values())
        total_likely = sum(e.likely for e in estimates.values())
        total_pessimistic = sum(e.pessimistic for e in estimates.values())
        
        pert_estimate = (total_optimistic + 4 * total_likely + total_pessimistic) / 6
        std_dev = (total_pessimistic - total_optimistic) / 6
        
        return {
            "optimisticHours": total_optimistic,
            "likelyHours": total_likely,
            "pessimisticHours": total_pessimistic,
            "pertEstimate": round(pert_estimate, 1),
            "standardDeviation": round(std_dev, 1),
            "confidence90": round(pert_estimate + (1.645 * std_dev), 1),
            "confidence95": round(pert_estimate + (1.96 * std_dev), 1)
        }
    
    def _generate_project_recommendations(self, analysis: List[Dict[str, Any]]) -> List[str]:
        """Generate project-level recommendations."""
        recommendations = []
        
        # Analyze complexity distribution
        high_complexity = sum(1 for a in analysis if a["score"] > 7)
        if high_complexity > len(analysis) * 0.3:
            recommendations.append(
                "Consider breaking down complex tasks into smaller pieces"
            )
        
        # Analyze risk distribution
        high_risk = sum(1 for a in analysis if a["riskAssessment"]["overallRiskLevel"] == "high")
        if high_risk > len(analysis) * 0.2:
            recommendations.append(
                "Implement additional risk monitoring and mitigation strategies"
            )
        
        # Analyze testing coverage
        missing_tests = sum(1 for a in analysis if a["factors"]["testing_complexity"] < 3)
        if missing_tests > len(analysis) * 0.3:
            recommendations.append(
                "Improve test coverage across tasks"
            )
        
        return recommendations
    
    def _generate_project_mitigations(self, risk_level: str, risk_factors: List[str]) -> List[str]:
        """Generate project-level risk mitigation strategies."""
        mitigations = []
        
        if risk_level == "high":
            mitigations.extend([
                "Implement weekly risk review meetings",
                "Set up automated monitoring and alerting",
                "Create detailed contingency plans for high-risk areas"
            ])
        elif risk_level == "medium":
            mitigations.extend([
                "Schedule regular risk assessment reviews",
                "Document and track known risks",
                "Prepare mitigation strategies for common issues"
            ])
        
        # Add specific mitigations based on common risk factors
        common_risks = self._identify_common_risks(risk_factors)
        for risk in common_risks:
            if "dependency" in risk.lower():
                mitigations.append(
                    "Review and optimize task dependencies"
                )
            elif "testing" in risk.lower():
                mitigations.append(
                    "Strengthen testing practices and infrastructure"
                )
        
        return mitigations 