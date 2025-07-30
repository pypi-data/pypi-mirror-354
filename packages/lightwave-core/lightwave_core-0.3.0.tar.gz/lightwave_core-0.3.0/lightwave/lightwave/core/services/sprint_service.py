"""Sprint management service implementation."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
import json

from ..models.sprint import Sprint, SprintStatus
from ..models.task import Task, TaskStatus
from .task_service import TaskService

class SprintError(Exception):
    """Base class for sprint-related errors."""
    pass

class SprintNotFoundError(SprintError):
    """Raised when a sprint is not found."""
    pass

class SprintService:
    """Service for managing sprints and their tasks."""

    def __init__(self, sprints_file: str = "sprints/sprints.json"):
        """Initialize sprint service.
        
        Args:
            sprints_file: Path to the sprints JSON file.
        """
        self.sprints_file = Path(sprints_file)
        self.task_service = TaskService()
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensure the sprints directory and file exist."""
        self.sprints_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.sprints_file.exists():
            self._save_sprints({})

    def _load_sprints(self) -> Dict[str, Sprint]:
        """Load sprints from JSON file."""
        try:
            with open(self.sprints_file, 'r') as f:
                data = json.load(f)
                return {
                    sprint_id: Sprint(**sprint_data)
                    for sprint_id, sprint_data in data.items()
                }
        except FileNotFoundError:
            return {}

    def _save_sprints(self, sprints: Dict[str, Any]) -> None:
        """Save sprints to JSON file."""
        with open(self.sprints_file, 'w') as f:
            json.dump(
                {sprint_id: sprint.to_dict() for sprint_id, sprint in sprints.items()},
                f,
                indent=2,
                default=str
            )

    def create_sprint(
        self,
        name: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Sprint:
        """Create a new sprint.
        
        Args:
            name: Sprint name
            description: Sprint description
            start_date: Sprint start date
            end_date: Sprint end date
            metadata: Additional metadata
            
        Returns:
            The created sprint.
            
        Raises:
            ValueError: If end_date is before start_date.
        """
        if end_date <= start_date:
            raise ValueError("End date must be after start date")

        sprints = self._load_sprints()
        sprint_id = f"sprint_{len(sprints) + 1}"
        
        sprint = Sprint(
            id=sprint_id,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            metadata=metadata or {}
        )
        
        sprints[sprint_id] = sprint
        self._save_sprints(sprints)
        return sprint

    def get_sprint(self, sprint_id: str) -> Sprint:
        """Get a sprint by ID.
        
        Args:
            sprint_id: The ID of the sprint to retrieve.
            
        Returns:
            The sprint with the specified ID.
            
        Raises:
            SprintNotFoundError: If the sprint is not found.
        """
        sprints = self._load_sprints()
        if sprint_id not in sprints:
            raise SprintNotFoundError(f"Sprint {sprint_id} not found")
        return sprints[sprint_id]

    def list_sprints(
        self,
        status_filter: Optional[SprintStatus] = None
    ) -> List[Sprint]:
        """List all sprints, optionally filtered by status.
        
        Args:
            status_filter: Optional status to filter sprints by.
            
        Returns:
            List of sprints matching the filter.
        """
        sprints = self._load_sprints()
        sprint_list = list(sprints.values())
        
        if status_filter:
            sprint_list = [s for s in sprint_list if s.status == status_filter]
            
        return sorted(sprint_list, key=lambda s: s.start_date)

    def update_sprint(
        self,
        sprint_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[SprintStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Sprint:
        """Update a sprint.
        
        Args:
            sprint_id: ID of the sprint to update
            name: New name
            description: New description
            status: New status
            start_date: New start date
            end_date: New end date
            metadata: New metadata
            
        Returns:
            The updated sprint.
            
        Raises:
            SprintNotFoundError: If the sprint is not found.
            ValueError: If end_date is before start_date.
        """
        sprints = self._load_sprints()
        if sprint_id not in sprints:
            raise SprintNotFoundError(f"Sprint {sprint_id} not found")
            
        sprint = sprints[sprint_id]
        
        if name is not None:
            sprint.name = name
        if description is not None:
            sprint.description = description
        if status is not None:
            sprint.status = status
            if status == SprintStatus.COMPLETED:
                sprint.calculate_velocity()
        if start_date is not None:
            sprint.start_date = start_date
        if end_date is not None:
            if start_date is None:
                start_date = sprint.start_date
            if end_date <= start_date:
                raise ValueError("End date must be after start date")
            sprint.end_date = end_date
        if metadata is not None:
            sprint.metadata = metadata
            
        sprint.updated_at = datetime.utcnow()
        self._save_sprints(sprints)
        return sprint

    def delete_sprint(self, sprint_id: str) -> bool:
        """Delete a sprint.
        
        Args:
            sprint_id: The ID of the sprint to delete.
            
        Returns:
            True if the sprint was deleted, False otherwise.
        """
        sprints = self._load_sprints()
        if sprint_id in sprints:
            del sprints[sprint_id]
            self._save_sprints(sprints)
            return True
        return False

    def add_task_to_sprint(self, sprint_id: str, task_id: int) -> Sprint:
        """Add a task to a sprint.
        
        Args:
            sprint_id: ID of the sprint
            task_id: ID of the task to add
            
        Returns:
            The updated sprint.
            
        Raises:
            SprintNotFoundError: If the sprint is not found.
            TaskNotFoundError: If the task is not found.
        """
        sprints = self._load_sprints()
        if sprint_id not in sprints:
            raise SprintNotFoundError(f"Sprint {sprint_id} not found")
            
        sprint = sprints[sprint_id]
        task = self.task_service.get_task(task_id)
        
        sprint.add_task(task)
        self._save_sprints(sprints)
        return sprint

    def remove_task_from_sprint(self, sprint_id: str, task_id: int) -> Sprint:
        """Remove a task from a sprint.
        
        Args:
            sprint_id: ID of the sprint
            task_id: ID of the task to remove
            
        Returns:
            The updated sprint.
            
        Raises:
            SprintNotFoundError: If the sprint is not found.
            TaskNotFoundError: If the task is not found.
        """
        sprints = self._load_sprints()
        if sprint_id not in sprints:
            raise SprintNotFoundError(f"Sprint {sprint_id} not found")
            
        sprint = sprints[sprint_id]
        task = self.task_service.get_task(task_id)
        
        sprint.remove_task(task)
        self._save_sprints(sprints)
        return sprint

    def get_sprint_metrics(self, sprint_id: str) -> Dict[str, Any]:
        """Get metrics for a sprint.
        
        Args:
            sprint_id: ID of the sprint
            
        Returns:
            Dictionary containing sprint metrics.
            
        Raises:
            SprintNotFoundError: If the sprint is not found.
        """
        sprint = self.get_sprint(sprint_id)
        
        return {
            "total_tasks": len(sprint.tasks),
            "completed_tasks": len(sprint.get_tasks_by_status(TaskStatus.DONE)),
            "blocked_tasks": len(sprint.get_blocked_tasks()),
            "ready_tasks": len(sprint.get_ready_tasks()),
            "story_points_total": sprint.story_points_total,
            "story_points_completed": sprint.story_points_completed,
            "completion_percentage": sprint.get_completion_percentage(),
            "velocity": sprint.velocity
        }

    def get_active_sprint(self) -> Optional[Sprint]:
        """Get the currently active sprint.
        
        Returns:
            The active sprint, or None if no sprint is active.
        """
        sprints = self._load_sprints()
        now = datetime.utcnow()
        
        active_sprints = [
            s for s in sprints.values()
            if s.status == SprintStatus.IN_PROGRESS
            and s.start_date <= now <= s.end_date
        ]
        
        return active_sprints[0] if active_sprints else None 