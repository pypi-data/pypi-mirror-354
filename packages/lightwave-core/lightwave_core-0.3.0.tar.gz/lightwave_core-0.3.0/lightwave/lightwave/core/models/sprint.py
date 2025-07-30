"""Sprint model for managing sprints in the LightWave CLI."""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from .task import Task, TaskStatus

class SprintStatus(str, Enum):
    """Valid sprint statuses."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Sprint(BaseModel):
    """Core sprint model."""
    id: str
    name: str
    description: str
    status: SprintStatus = SprintStatus.PLANNING
    start_date: datetime
    end_date: datetime
    tasks: List[Task] = Field(default_factory=list)
    velocity: Optional[float] = None
    story_points_completed: float = 0
    story_points_total: float = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        """Add a task to the sprint."""
        if task not in self.tasks:
            self.tasks.append(task)
            self.story_points_total += task.metadata.get("story_points", 0)
            self.updated_at = datetime.utcnow()

    def remove_task(self, task: Task) -> bool:
        """Remove a task from the sprint."""
        if task in self.tasks:
            self.tasks.remove(task)
            self.story_points_total -= task.metadata.get("story_points", 0)
            if task.status == TaskStatus.DONE:
                self.story_points_completed -= task.metadata.get("story_points", 0)
            self.updated_at = datetime.utcnow()
            return True
        return False

    def update_task_status(self, task: Task, new_status: TaskStatus) -> None:
        """Update a task's status and recalculate sprint metrics."""
        if task in self.tasks:
            old_status = task.status
            task.status = new_status
            story_points = task.metadata.get("story_points", 0)
            
            # Update completed story points
            if old_status != TaskStatus.DONE and new_status == TaskStatus.DONE:
                self.story_points_completed += story_points
            elif old_status == TaskStatus.DONE and new_status != TaskStatus.DONE:
                self.story_points_completed -= story_points
            
            self.updated_at = datetime.utcnow()

    def get_completion_percentage(self) -> float:
        """Get the percentage of completed story points."""
        if self.story_points_total == 0:
            return 0.0
        return (self.story_points_completed / self.story_points_total) * 100

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status."""
        return [t for t in self.tasks if t.status == status]

    def get_blocked_tasks(self) -> List[Task]:
        """Get all tasks that are blocked by dependencies."""
        completed_task_ids = [t.id for t in self.get_tasks_by_status(TaskStatus.DONE)]
        return [t for t in self.tasks if t.is_blocked(completed_task_ids)]

    def get_ready_tasks(self) -> List[Task]:
        """Get all tasks that are ready to be worked on (not blocked and not done)."""
        completed_task_ids = [t.id for t in self.get_tasks_by_status(TaskStatus.DONE)]
        return [
            t for t in self.tasks 
            if t.status != TaskStatus.DONE and not t.is_blocked(completed_task_ids)
        ]

    def calculate_velocity(self) -> None:
        """Calculate sprint velocity based on completed story points."""
        if self.status == SprintStatus.COMPLETED:
            self.velocity = self.story_points_completed
            self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert sprint to a dictionary for storage."""
        return {
            **self.dict(exclude={"created_at", "updated_at"}),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tasks": [t.to_dict() for t in self.tasks]
        } 