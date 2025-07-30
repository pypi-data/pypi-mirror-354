"""
Sprint-specific task complexity analysis with workflow context awareness.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import yaml
from pathlib import Path

from .complexity_analyzer import ComplexityAnalyzer, ComplexityMetrics
from ..models.task import Task
from ..models.dependency_graph import DependencyGraph

@dataclass
class SprintContext:
    """Sprint context information."""
    sprint_name: str
    sprint_goal: str
    start_date: datetime
    end_date: datetime
    velocity: float
    capacity: float
    team_size: int
    workflow_states: List[str]

@dataclass
class SprintComplexityMetrics(ComplexityMetrics):
    """Extended complexity metrics for sprint tasks."""
    workflow_complexity: float = 0.0
    state_transition_risk: float = 0.0
    sprint_capacity_impact: float = 0.0
    team_familiarity: float = 0.0
    sprint_goal_alignment: float = 0.0

class SprintComplexityAnalyzer(ComplexityAnalyzer):
    """Enhanced complexity analyzer for sprint tasks with workflow context."""
    
    WORKFLOW_STATES = [
        "Open",
        "Considering",
        "Scoping",
        "Prioritized",
        "In Design",
        "In Development",
        "In Review",
        "Ready for Deployment"
    ]
    
    def __init__(
        self,
        dependency_graph: DependencyGraph,
        sprint_context: SprintContext,
        config_dir: str = "lightwave-config"
    ):
        """Initialize the sprint complexity analyzer.
        
        Args:
            dependency_graph: Task dependency graph
            sprint_context: Current sprint context
            config_dir: Directory containing configuration files
        """
        super().__init__(dependency_graph)
        self.sprint_context = sprint_context
        self.config_dir = Path(config_dir)
        self._load_configurations()
    
    def _load_configurations(self) -> None:
        """Load sprint-related configurations."""
        try:
            # Load standard configuration
            with open(self.config_dir / "lightwave-config-standard.yaml") as f:
                self.standard_config = yaml.safe_load(f)
            
            # Load sprint context boilerplate
            with open(self.config_dir / "lightwave-sprint-context/boilerplate.yml") as f:
                self.sprint_boilerplate = yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load all configuration files: {e}")
            self.standard_config = {}
            self.sprint_boilerplate = {}
    
    def analyze_sprint_task(self, task: Task) -> Dict[str, Any]:
        """Analyze a task in the context of the current sprint.
        
        Args:
            task: The task to analyze
            
        Returns:
            Dictionary containing sprint-specific complexity analysis
        """
        # Get base complexity analysis
        base_analysis = self.analyze_task(task)
        
        # Calculate sprint-specific metrics
        sprint_metrics = self._calculate_sprint_metrics(task)
        
        # Merge base metrics with sprint metrics
        metrics = {**base_analysis['metrics']}
        metrics.update({
            'workflow_complexity': sprint_metrics.workflow_complexity,
            'state_transition_risk': sprint_metrics.state_transition_risk,
            'sprint_capacity_impact': sprint_metrics.sprint_capacity_impact,
            'team_familiarity': sprint_metrics.team_familiarity,
            'sprint_goal_alignment': sprint_metrics.sprint_goal_alignment
        })
        
        # Adjust overall complexity based on sprint context
        sprint_complexity_score = self._calculate_sprint_complexity_score(sprint_metrics)
        adjusted_complexity = self._adjust_complexity_for_sprint(
            base_analysis['overall_complexity'],
            sprint_complexity_score
        )
        
        # Generate sprint-specific recommendations
        sprint_recommendations = self._generate_sprint_recommendations(
            task,
            sprint_metrics,
            base_analysis['recommendations']
        )
        
        return {
            **base_analysis,
            'metrics': metrics,
            'overall_complexity': adjusted_complexity,
            'sprint_specific': {
                'workflow_state': task.status,
                'sprint_impact': self._assess_sprint_impact(sprint_metrics),
                'state_transitions': self._analyze_state_transitions(task),
                'capacity_utilization': self._calculate_capacity_utilization(task),
                'goal_alignment': self._assess_goal_alignment(task)
            },
            'recommendations': sprint_recommendations
        }
    
    def _calculate_sprint_metrics(self, task: Task) -> SprintComplexityMetrics:
        """Calculate sprint-specific complexity metrics."""
        base_metrics = self._calculate_base_metrics(task)
        
        workflow_complexity = self._calculate_workflow_complexity(task)
        state_transition_risk = self._calculate_state_transition_risk(task)
        sprint_capacity_impact = self._calculate_capacity_impact(task)
        team_familiarity = self._calculate_team_familiarity(task)
        sprint_goal_alignment = self._calculate_goal_alignment(task)
        
        return SprintComplexityMetrics(
            **base_metrics.__dict__,
            workflow_complexity=workflow_complexity,
            state_transition_risk=state_transition_risk,
            sprint_capacity_impact=sprint_capacity_impact,
            team_familiarity=team_familiarity,
            sprint_goal_alignment=sprint_goal_alignment
        )
    
    def _calculate_workflow_complexity(self, task: Task) -> float:
        """Calculate complexity based on workflow state and transitions."""
        # Base complexity based on current state
        state_index = self.WORKFLOW_STATES.index(task.status)
        base_score = (state_index + 1) / len(self.WORKFLOW_STATES) * 5.0
        
        # Add complexity for each state transition
        transitions = len(self._get_state_transitions(task))
        transition_score = min(5.0, transitions * 0.5)
        
        return min(10.0, base_score + transition_score)
    
    def _calculate_state_transition_risk(self, task: Task) -> float:
        """Calculate risk based on state transitions."""
        transitions = self._get_state_transitions(task)
        if not transitions:
            return 0.0
        
        risk_score = 0.0
        
        # Analyze transition patterns
        backwards_transitions = sum(
            1 for i in range(len(transitions) - 1)
            if self.WORKFLOW_STATES.index(transitions[i+1]) <
            self.WORKFLOW_STATES.index(transitions[i])
        )
        
        # Penalize backwards transitions
        risk_score += backwards_transitions * 2.0
        
        # Add risk for frequent state changes
        if len(transitions) > 3:
            risk_score += (len(transitions) - 3) * 0.5
        
        return min(10.0, risk_score)
    
    def _calculate_capacity_impact(self, task: Task) -> float:
        """Calculate impact on sprint capacity."""
        # Base impact from time estimate
        time_estimate = self._estimate_time(task)
        base_impact = time_estimate['expected'].total_seconds() / 3600
        
        # Normalize to sprint capacity
        capacity_impact = base_impact / self.sprint_context.capacity
        
        # Add impact for dependencies
        dependency_factor = 1.0 + (len(task.dependencies) * 0.1)
        
        return min(10.0, capacity_impact * dependency_factor * 5.0)
    
    def _calculate_team_familiarity(self, task: Task) -> float:
        """Calculate team familiarity with task type."""
        # TODO: Implement team familiarity calculation based on historical data
        return 5.0  # Default medium familiarity
    
    def _calculate_goal_alignment(self, task: Task) -> float:
        """Calculate alignment with sprint goals."""
        if not self.sprint_context.sprint_goal:
            return 5.0
        
        # Calculate text similarity between task and sprint goal
        goal_similarity = self._calculate_text_similarity(
            f"{task.title} {task.description or ''}",
            self.sprint_context.sprint_goal
        )
        
        return goal_similarity * 10.0
    
    def _calculate_sprint_complexity_score(self, metrics: SprintComplexityMetrics) -> float:
        """Calculate overall sprint-specific complexity score."""
        weights = {
            'workflow_complexity': 0.2,
            'state_transition_risk': 0.15,
            'sprint_capacity_impact': 0.25,
            'team_familiarity': 0.15,
            'sprint_goal_alignment': 0.25
        }
        
        return sum(
            getattr(metrics, key) * weight
            for key, weight in weights.items()
        )
    
    def _adjust_complexity_for_sprint(
        self,
        base_complexity: str,
        sprint_score: float
    ) -> str:
        """Adjust complexity level based on sprint context."""
        # Convert base complexity to numeric score
        base_score = {
            'LOW': 2,
            'MEDIUM': 5,
            'HIGH': 8
        }.get(base_complexity, 5)
        
        # Blend base complexity with sprint score
        final_score = (base_score * 0.6) + (sprint_score * 0.4)
        
        # Convert back to level
        if final_score <= 3:
            return 'LOW'
        elif final_score <= 7:
            return 'MEDIUM'
        else:
            return 'HIGH'
    
    def _assess_sprint_impact(self, metrics: SprintComplexityMetrics) -> Dict[str, Any]:
        """Assess task's impact on sprint success."""
        capacity_risk = 'HIGH' if metrics.sprint_capacity_impact > 7 else \
                       'MEDIUM' if metrics.sprint_capacity_impact > 4 else 'LOW'
        
        return {
            'capacity_risk': capacity_risk,
            'goal_alignment_score': round(metrics.sprint_goal_alignment, 2),
            'team_readiness': round(metrics.team_familiarity, 2),
            'workflow_risk': round(metrics.workflow_complexity, 2)
        }
    
    def _analyze_state_transitions(self, task: Task) -> Dict[str, Any]:
        """Analyze task state transitions."""
        transitions = self._get_state_transitions(task)
        
        return {
            'current_state': task.status,
            'transition_count': len(transitions),
            'has_backwards_transitions': any(
                self.WORKFLOW_STATES.index(transitions[i+1]) <
                self.WORKFLOW_STATES.index(transitions[i])
                for i in range(len(transitions) - 1)
            ) if len(transitions) > 1 else False,
            'state_history': transitions
        }
    
    def _calculate_capacity_utilization(self, task: Task) -> Dict[str, Any]:
        """Calculate task's impact on sprint capacity."""
        time_estimate = self._estimate_time(task)
        task_hours = time_estimate['expected'].total_seconds() / 3600
        
        return {
            'hours_estimate': round(task_hours, 1),
            'capacity_percentage': round(
                (task_hours / self.sprint_context.capacity) * 100, 1
            ),
            'remaining_capacity': round(
                self.sprint_context.capacity - task_hours, 1
            )
        }
    
    def _assess_goal_alignment(self, task: Task) -> Dict[str, Any]:
        """Assess how well the task aligns with sprint goals."""
        return {
            'alignment_score': round(self._calculate_goal_alignment(task), 2),
            'sprint_goal': self.sprint_context.sprint_goal,
            'contributes_to_goal': self._calculate_goal_alignment(task) > 7.0
        }
    
    def _get_state_transitions(self, task: Task) -> List[str]:
        """Get list of state transitions for a task."""
        # TODO: Implement state transition history tracking
        return [task.status]  # Currently only returns current state
    
    def _generate_sprint_recommendations(
        self,
        task: Task,
        metrics: SprintComplexityMetrics,
        base_recommendations: List[str]
    ) -> List[str]:
        """Generate sprint-specific recommendations."""
        recommendations = base_recommendations.copy()
        
        # Capacity-based recommendations
        if metrics.sprint_capacity_impact > 7.0:
            recommendations.append(
                "Consider splitting task across multiple sprints due to high capacity impact"
            )
        
        # Workflow-based recommendations
        if metrics.workflow_complexity > 7.0:
            recommendations.append(
                "Simplify task workflow by reducing state transitions"
            )
        
        # Team familiarity recommendations
        if metrics.team_familiarity < 4.0:
            recommendations.append(
                "Schedule knowledge sharing sessions to improve team familiarity"
            )
        
        # Goal alignment recommendations
        if metrics.sprint_goal_alignment < 5.0:
            recommendations.append(
                "Review task alignment with sprint goals"
            )
        
        return recommendations
    
    def analyze_sprint_tasks(self) -> Dict[str, Any]:
        """Analyze all tasks in the current sprint."""
        task_analyses = []
        sprint_metrics = {
            'total_tasks': 0,
            'total_story_points': 0,
            'capacity_utilization': 0.0,
            'risk_distribution': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
            'state_distribution': {},
            'goal_alignment_avg': 0.0
        }
        
        for task in self.dependency_graph.tasks.values():
            analysis = self.analyze_sprint_task(task)
            task_analyses.append(analysis)
            
            # Update sprint metrics
            sprint_metrics['total_tasks'] += 1
            sprint_metrics['risk_distribution'][analysis['overall_complexity']] += 1
            
            state = analysis['sprint_specific']['workflow_state']
            sprint_metrics['state_distribution'][state] = \
                sprint_metrics['state_distribution'].get(state, 0) + 1
            
            sprint_metrics['goal_alignment_avg'] += \
                analysis['sprint_specific']['goal_alignment']['alignment_score']
        
        if sprint_metrics['total_tasks'] > 0:
            sprint_metrics['goal_alignment_avg'] /= sprint_metrics['total_tasks']
        
        return {
            'sprint_name': self.sprint_context.sprint_name,
            'sprint_goal': self.sprint_context.sprint_goal,
            'sprint_dates': {
                'start': self.sprint_context.start_date.isoformat(),
                'end': self.sprint_context.end_date.isoformat()
            },
            'metrics': sprint_metrics,
            'task_analyses': task_analyses,
            'recommendations': self._generate_sprint_recommendations(
                task_analyses,
                sprint_metrics
            )
        }
    
    def _generate_sprint_recommendations(
        self,
        task_analyses: List[Dict[str, Any]],
        sprint_metrics: Dict[str, Any]
    ) -> List[str]:
        """Generate sprint-level recommendations."""
        recommendations = []
        
        # Risk distribution recommendations
        high_risk_percentage = (
            sprint_metrics['risk_distribution']['HIGH'] /
            sprint_metrics['total_tasks']
        ) if sprint_metrics['total_tasks'] > 0 else 0
        
        if high_risk_percentage > 0.3:
            recommendations.append(
                "High proportion of high-risk tasks. Consider rebalancing sprint"
            )
        
        # Goal alignment recommendations
        if sprint_metrics['goal_alignment_avg'] < 6.0:
            recommendations.append(
                "Low average goal alignment. Review task selection against sprint goals"
            )
        
        # State distribution recommendations
        in_progress_states = ['In Design', 'In Development', 'In Review']
        in_progress_count = sum(
            sprint_metrics['state_distribution'].get(state, 0)
            for state in in_progress_states
        )
        
        if in_progress_count > self.sprint_context.team_size * 1.5:
            recommendations.append(
                "Too many tasks in progress. Focus on completing existing work"
            )
        
        return recommendations 