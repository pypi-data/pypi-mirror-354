"""
Machine learning-based complexity prediction for tasks.
"""
from typing import Dict, List, Any
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

from ..models.task import Task, TaskStatus, TaskPriority

class MLComplexityPredictor:
    """Predicts task complexity using machine learning."""
    
    def __init__(self, model_path: str = "models/complexity_model.joblib"):
        """Initialize the predictor.
        
        Args:
            model_path: Path to the saved model file
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self._load_or_create_model()
    
    def _load_or_create_model(self) -> None:
        """Load existing model or create a new one if not found."""
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
        except FileNotFoundError:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
    
    def _extract_features(self, task: Task) -> np.ndarray:
        """Extract numerical features from a task for prediction."""
        features = [
            len(task.dependencies),
            len(task.subtasks),
            len(task.description or ''),
            TaskPriority[task.priority.upper()].value,
            len(task.test_strategy or '') if task.test_strategy else 0,
            # Text complexity features
            self._calculate_text_complexity(task.title),
            self._calculate_text_complexity(task.description or ''),
            # Structural features
            self._calculate_structural_complexity(task),
            # Historical features
            self._get_historical_complexity(task)
        ]
        return np.array(features).reshape(1, -1)
    
    def _calculate_text_complexity(self, text: str) -> float:
        """Calculate complexity score based on text content."""
        complexity_indicators = {
            'high': ['complex', 'difficult', 'challenging', 'advanced', 'optimize', 'refactor'],
            'medium': ['implement', 'create', 'develop', 'integrate', 'update'],
            'low': ['fix', 'add', 'remove', 'change', 'test']
        }
        
        score = 0.0
        text = text.lower()
        
        for level, indicators in complexity_indicators.items():
            count = sum(1 for ind in indicators if ind in text)
            if level == 'high':
                score += count * 2.0
            elif level == 'medium':
                score += count * 1.0
            else:
                score += count * 0.5
                
        return min(10.0, score)
    
    def _calculate_structural_complexity(self, task: Task) -> float:
        """Calculate complexity based on task structure."""
        score = 0.0
        
        # Subtask depth and breadth
        if task.subtasks:
            max_depth = self._get_subtask_depth(task)
            score += max_depth * 1.5
            score += len(task.subtasks) * 0.5
        
        # Dependency complexity
        if task.dependencies:
            score += len(task.dependencies) * 1.0
            
        return min(10.0, score)
    
    def _get_subtask_depth(self, task: Task, current_depth: int = 1) -> int:
        """Calculate maximum depth of subtask hierarchy."""
        if not task.subtasks:
            return current_depth
            
        return max(
            self._get_subtask_depth(subtask, current_depth + 1)
            for subtask in task.subtasks
        )
    
    def _get_historical_complexity(self, task: Task) -> float:
        """Get complexity score based on historical data."""
        # TODO: Implement historical data analysis
        return 5.0  # Default medium complexity
    
    def predict_complexity(self, task: Task) -> Dict[str, Any]:
        """Predict complexity metrics for a task."""
        features = self._extract_features(task)
        
        if self.scaler is not None:
            features = self.scaler.transform(features)
            
        predicted_complexity = float(self.model.predict(features)[0])
        
        # Calculate prediction confidence
        if hasattr(self.model, 'estimators_'):
            predictions = [
                estimator.predict(features)[0]
                for estimator in self.model.estimators_
            ]
            confidence = 1.0 - (np.std(predictions) / np.mean(predictions))
        else:
            confidence = 0.8  # Default confidence for new model
            
        return {
            'predicted_complexity': round(predicted_complexity, 2),
            'confidence': round(confidence, 2),
            'features_used': [
                'dependencies_count',
                'subtasks_count',
                'description_length',
                'priority_level',
                'test_strategy_length',
                'title_complexity',
                'description_complexity',
                'structural_complexity',
                'historical_complexity'
            ]
        }
    
    def train(self, tasks: List[Task], actual_complexities: List[float]) -> None:
        """Train the model with new data.
        
        Args:
            tasks: List of tasks to train on
            actual_complexities: Corresponding actual complexity scores
        """
        if not tasks or not actual_complexities:
            return
            
        features = np.vstack([
            self._extract_features(task).flatten()
            for task in tasks
        ])
        
        # Scale features
        self.scaler = StandardScaler().fit(features)
        scaled_features = self.scaler.transform(features)
        
        # Train model
        self.model.fit(scaled_features, actual_complexities)
        
        # Save model
        self._save_model()
    
    def _save_model(self) -> None:
        """Save the trained model and scaler."""
        model_dir = Path(self.model_path).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(
            {
                'model': self.model,
                'scaler': self.scaler
            },
            self.model_path
        ) 