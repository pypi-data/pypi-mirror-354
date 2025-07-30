"""
Historical task data analysis for improving complexity and time estimates.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

from ..models.task import Task, TaskStatus

class TaskHistoryAnalyzer:
    """Analyzes historical task data to improve estimates."""
    
    def __init__(self):
        self.task_history: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        self.completion_times: Dict[int, timedelta] = {}
        self.accuracy_metrics: Dict[int, Dict[str, float]] = {}
    
    def record_task_update(self, task: Task, update_type: str, details: Dict[str, Any]) -> None:
        """Record a task update for historical analysis.
        
        Args:
            task: The task being updated
            update_type: Type of update (e.g., 'status_change', 'estimate_update')
            details: Additional details about the update
        """
        self.task_history[task.id].append({
            'timestamp': datetime.utcnow(),
            'update_type': update_type,
            'task_status': task.status,
            'details': details
        })
        
        # Record completion time if task is done
        if update_type == 'status_change' and task.status == TaskStatus.DONE:
            self._calculate_completion_time(task.id)
    
    def _calculate_completion_time(self, task_id: int) -> None:
        """Calculate actual completion time for a task."""
        history = self.task_history[task_id]
        if not history:
            return
            
        start_time = None
        end_time = None
        
        for event in history:
            if event['update_type'] == 'status_change':
                if event['details'].get('from_status') == TaskStatus.PENDING:
                    start_time = event['timestamp']
                elif event['task_status'] == TaskStatus.DONE:
                    end_time = event['timestamp']
        
        if start_time and end_time:
            self.completion_times[task_id] = end_time - start_time
    
    def analyze_estimation_accuracy(self, task_id: int) -> Optional[Dict[str, float]]:
        """Analyze accuracy of time and complexity estimates for a task.
        
        Args:
            task_id: ID of the task to analyze
            
        Returns:
            Dictionary with accuracy metrics or None if insufficient data
        """
        if task_id not in self.completion_times:
            return None
            
        history = self.task_history[task_id]
        initial_estimates = next(
            (event['details'] for event in history
             if event['update_type'] == 'initial_estimate'),
            None
        )
        
        if not initial_estimates:
            return None
            
        actual_hours = self.completion_times[task_id].total_seconds() / 3600
        estimated_hours = initial_estimates.get('estimated_hours', 0)
        
        accuracy = {
            'time_estimate_accuracy': self._calculate_estimate_accuracy(
                estimated_hours, actual_hours
            ),
            'complexity_estimate_accuracy': self._analyze_complexity_accuracy(
                task_id, initial_estimates.get('estimated_complexity', 0)
            )
        }
        
        self.accuracy_metrics[task_id] = accuracy
        return accuracy
    
    def _calculate_estimate_accuracy(self, estimated: float, actual: float) -> float:
        """Calculate accuracy of a numerical estimate."""
        if estimated == 0:
            return 0.0
        
        error = abs(actual - estimated) / estimated
        return max(0.0, 1.0 - error)
    
    def _analyze_complexity_accuracy(self, task_id: int, estimated_complexity: float) -> float:
        """Analyze accuracy of complexity estimate based on actual task history."""
        history = self.task_history[task_id]
        
        # Indicators that might suggest higher actual complexity
        complexity_indicators = {
            'status_changes': len([
                e for e in history
                if e['update_type'] == 'status_change'
            ]),
            'blockers': len([
                e for e in history
                if e['update_type'] == 'blocker_added'
            ]),
            'estimate_updates': len([
                e for e in history
                if e['update_type'] == 'estimate_update'
            ])
        }
        
        # Calculate actual complexity score
        actual_complexity = (
            complexity_indicators['status_changes'] * 0.5 +
            complexity_indicators['blockers'] * 2.0 +
            complexity_indicators['estimate_updates'] * 1.0
        )
        
        return self._calculate_estimate_accuracy(
            estimated_complexity,
            min(10.0, actual_complexity)
        )
    
    def get_historical_metrics(self, task: Task) -> Dict[str, Any]:
        """Get historical metrics for similar tasks.
        
        Args:
            task: Task to find historical metrics for
            
        Returns:
            Dictionary containing historical metrics and patterns
        """
        similar_tasks = self._find_similar_tasks(task)
        
        if not similar_tasks:
            return {
                'available': False,
                'message': 'No similar tasks found in history'
            }
        
        completion_times = [
            self.completion_times[t_id]
            for t_id in similar_tasks
            if t_id in self.completion_times
        ]
        
        accuracy_metrics = [
            self.accuracy_metrics[t_id]
            for t_id in similar_tasks
            if t_id in self.accuracy_metrics
        ]
        
        if not completion_times:
            return {
                'available': False,
                'message': 'No completion time data for similar tasks'
            }
        
        return {
            'available': True,
            'similar_task_count': len(similar_tasks),
            'avg_completion_time': self._calculate_average_timedelta(completion_times),
            'completion_time_std': self._calculate_timedelta_std(completion_times),
            'estimate_accuracy': self._aggregate_accuracy_metrics(accuracy_metrics),
            'patterns': self._identify_patterns(similar_tasks)
        }
    
    def _find_similar_tasks(self, task: Task) -> List[int]:
        """Find historically similar tasks based on various criteria."""
        similar_tasks = []
        
        for task_id, history in self.task_history.items():
            if task_id == task.id:
                continue
                
            # Get the initial state of the historical task
            initial_state = next(
                (event['details'] for event in history
                 if event['update_type'] == 'initial_state'),
                None
            )
            
            if not initial_state:
                continue
            
            # Calculate similarity score
            similarity_score = self._calculate_task_similarity(
                task,
                initial_state
            )
            
            if similarity_score >= 0.7:  # 70% similarity threshold
                similar_tasks.append(task_id)
        
        return similar_tasks
    
    def _calculate_task_similarity(self, task: Task, historical_state: Dict[str, Any]) -> float:
        """Calculate similarity score between two tasks."""
        scores = []
        
        # Compare number of dependencies
        if len(task.dependencies) > 0 or historical_state.get('dependency_count', 0) > 0:
            dep_similarity = 1.0 - abs(
                len(task.dependencies) - historical_state.get('dependency_count', 0)
            ) / max(len(task.dependencies), historical_state.get('dependency_count', 1))
            scores.append(dep_similarity)
        
        # Compare number of subtasks
        if len(task.subtasks) > 0 or historical_state.get('subtask_count', 0) > 0:
            subtask_similarity = 1.0 - abs(
                len(task.subtasks) - historical_state.get('subtask_count', 0)
            ) / max(len(task.subtasks), historical_state.get('subtask_count', 1))
            scores.append(subtask_similarity)
        
        # Compare priority
        if task.priority == historical_state.get('priority'):
            scores.append(1.0)
        
        # Compare text similarity
        text_similarity = self._calculate_text_similarity(
            f"{task.title} {task.description or ''}",
            historical_state.get('text', '')
        )
        scores.append(text_similarity)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings."""
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _calculate_average_timedelta(self, deltas: List[timedelta]) -> timedelta:
        """Calculate average of a list of timedeltas."""
        if not deltas:
            return timedelta()
            
        total_seconds = sum(d.total_seconds() for d in deltas)
        return timedelta(seconds=total_seconds / len(deltas))
    
    def _calculate_timedelta_std(self, deltas: List[timedelta]) -> timedelta:
        """Calculate standard deviation of a list of timedeltas."""
        if not deltas:
            return timedelta()
            
        seconds = [d.total_seconds() for d in deltas]
        return timedelta(seconds=float(np.std(seconds)))
    
    def _aggregate_accuracy_metrics(self, metrics: List[Dict[str, float]]) -> Dict[str, float]:
        """Aggregate accuracy metrics from multiple tasks."""
        if not metrics:
            return {
                'time_estimate_accuracy': 0.0,
                'complexity_estimate_accuracy': 0.0
            }
            
        return {
            'time_estimate_accuracy': np.mean([
                m['time_estimate_accuracy'] for m in metrics
            ]),
            'complexity_estimate_accuracy': np.mean([
                m['complexity_estimate_accuracy'] for m in metrics
            ])
        }
    
    def _identify_patterns(self, task_ids: List[int]) -> List[Dict[str, Any]]:
        """Identify common patterns in similar tasks."""
        patterns = []
        
        # Analyze common blockers
        blocker_counts = defaultdict(int)
        for task_id in task_ids:
            for event in self.task_history[task_id]:
                if event['update_type'] == 'blocker_added':
                    blocker_type = event['details'].get('blocker_type')
                    if blocker_type:
                        blocker_counts[blocker_type] += 1
        
        common_blockers = [
            {'type': b_type, 'count': count}
            for b_type, count in blocker_counts.items()
            if count >= len(task_ids) * 0.3  # Present in 30% of similar tasks
        ]
        
        if common_blockers:
            patterns.append({
                'pattern_type': 'common_blockers',
                'description': 'Common blockers in similar tasks',
                'details': common_blockers
            })
        
        # Analyze status transition patterns
        status_patterns = self._analyze_status_patterns(task_ids)
        if status_patterns:
            patterns.append({
                'pattern_type': 'status_transitions',
                'description': 'Common status transition patterns',
                'details': status_patterns
            })
        
        return patterns
    
    def _analyze_status_patterns(self, task_ids: List[int]) -> List[Dict[str, Any]]:
        """Analyze common status transition patterns."""
        transition_counts = defaultdict(int)
        
        for task_id in task_ids:
            status_changes = [
                event for event in self.task_history[task_id]
                if event['update_type'] == 'status_change'
            ]
            
            for i in range(len(status_changes) - 1):
                from_status = status_changes[i]['task_status']
                to_status = status_changes[i + 1]['task_status']
                transition_counts[f"{from_status}->{to_status}"] += 1
        
        return [
            {
                'transition': transition,
                'count': count,
                'frequency': count / len(task_ids)
            }
            for transition, count in transition_counts.items()
            if count >= len(task_ids) * 0.3  # Present in 30% of similar tasks
        ] 