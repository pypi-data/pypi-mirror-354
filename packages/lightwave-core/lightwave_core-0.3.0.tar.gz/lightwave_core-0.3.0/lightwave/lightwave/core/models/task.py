"""Task models for the Lightwave ecosystem."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import Field

from .base import BaseModel


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    def __lt__(self, other):
        """Enable comparison of priorities."""
        if not isinstance(other, TaskPriority):
            return NotImplemented
        order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return order[self.value] < order[other.value]
    
    def __gt__(self, other):
        """Enable greater than comparison of priorities."""
        if not isinstance(other, TaskPriority):
            return NotImplemented
        order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return order[self.value] > order[other.value]


class SubTask(BaseModel):
    """Subtask model for breaking down tasks into smaller components."""
    
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique subtask identifier")
    title: str = Field(..., description="Subtask title")
    description: Optional[str] = Field(default=None, description="Detailed subtask description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status")
    dependencies: List[str] = Field(default_factory=list, description="List of subtask IDs this depends on")
    assigned_to: Optional[str] = Field(default=None, description="Person assigned to this subtask")
    estimated_hours: Optional[float] = Field(default=None, description="Estimated hours to complete")
    actual_hours: Optional[float] = Field(default=None, description="Actual hours spent")
    notes: Optional[str] = Field(default=None, description="Additional notes or progress updates")
    
    def update_status(self, new_status: TaskStatus) -> None:
        """Update subtask status with timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def is_blocked(self, completed_subtask_ids: List[str]) -> bool:
        """Check if subtask is blocked by uncompleted dependencies."""
        return any(dep_id not in completed_subtask_ids for dep_id in self.dependencies)
    
    def can_start(self, completed_subtask_ids: List[str]) -> bool:
        """Check if subtask can be started (all dependencies completed)."""
        return (
            self.status == TaskStatus.PENDING and
            not self.is_blocked(completed_subtask_ids)
        )


class Task(BaseModel):
    """Main task model for the Lightwave ecosystem."""
    
    id: Union[str, int] = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    
    # Task organization
    sprint: Optional[str] = Field(default=None, description="Sprint identifier")
    epic: Optional[str] = Field(default=None, description="Epic identifier")
    labels: List[str] = Field(default_factory=list, description="Task labels/tags")
    
    # People and assignments
    assigned_to: Optional[str] = Field(default=None, description="Person assigned to this task")
    reporter: Optional[str] = Field(default=None, description="Person who created the task")
    reviewer: Optional[str] = Field(default=None, description="Person who will review the task")
    
    # Dependencies and relationships
    dependencies: List[int] = Field(default_factory=list, description="List of task IDs this task depends on")
    blockers: List[int] = Field(default_factory=list, description="List of task IDs that block this task")
    
    # Implementation details
    details: Optional[str] = Field(default=None, description="Detailed implementation notes")
    test_strategy: Optional[str] = Field(default=None, description="Testing strategy and approach")
    acceptance_criteria: List[str] = Field(default_factory=list, description="Acceptance criteria checklist")
    
    # Time tracking
    estimated_hours: Optional[float] = Field(default=None, description="Estimated hours to complete")
    actual_hours: Optional[float] = Field(default=None, description="Actual hours spent")
    due_date: Optional[datetime] = Field(default=None, description="Task due date")
    
    # Subtasks
    subtasks: List[SubTask] = Field(default_factory=list, description="List of subtasks")
    
    # Additional metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def update_status(self, new_status: TaskStatus) -> None:
        """Update task status with timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def is_blocked(self, completed_task_ids: List[int]) -> bool:
        """Check if task is blocked by uncompleted dependencies."""
        return any(dep_id not in completed_task_ids for dep_id in self.dependencies)
    
    def can_start(self, completed_task_ids: List[int]) -> bool:
        """Check if task can be started (all dependencies completed)."""
        return (
            self.status == TaskStatus.PENDING and
            not self.is_blocked(completed_task_ids)
        )
    
    def add_subtask(
        self, 
        title: str, 
        description: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ) -> SubTask:
        """Add a new subtask to this task."""
        subtask = SubTask(
            title=title,
            description=description,
            dependencies=dependencies or []
        )
        self.subtasks.append(subtask)
        self.updated_at = datetime.utcnow()
        return subtask
    
    def get_subtask(self, subtask_id: str) -> Optional[SubTask]:
        """Get a subtask by ID."""
        return next((st for st in self.subtasks if st.id == subtask_id), None)
    
    def remove_subtask(self, subtask_id: str) -> bool:
        """Remove a subtask by ID."""
        original_count = len(self.subtasks)
        self.subtasks = [st for st in self.subtasks if st.id != subtask_id]
        if len(self.subtasks) < original_count:
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def get_ready_subtasks(self) -> List[SubTask]:
        """Get all subtasks that are ready to be worked on."""
        completed_subtask_ids = [
            st.id for st in self.subtasks 
            if st.status == TaskStatus.DONE
        ]
        
        return [
            st for st in self.subtasks 
            if st.can_start(completed_subtask_ids)
        ]
    
    def get_blocked_subtasks(self) -> List[SubTask]:
        """Get all subtasks that are blocked by dependencies."""
        completed_subtask_ids = [
            st.id for st in self.subtasks 
            if st.status == TaskStatus.DONE
        ]
        
        return [
            st for st in self.subtasks 
            if st.status == TaskStatus.PENDING and st.is_blocked(completed_subtask_ids)
        ]
    
    def get_completion_percentage(self) -> float:
        """Get task completion percentage based on subtasks."""
        if not self.subtasks:
            return 100.0 if self.status == TaskStatus.DONE else 0.0
        
        completed_count = sum(
            1 for st in self.subtasks 
            if st.status == TaskStatus.DONE
        )
        return (completed_count / len(self.subtasks)) * 100.0
    
    def add_acceptance_criterion(self, criterion: str) -> None:
        """Add an acceptance criterion."""
        if criterion not in self.acceptance_criteria:
            self.acceptance_criteria.append(criterion)
            self.updated_at = datetime.utcnow()
    
    def remove_acceptance_criterion(self, criterion: str) -> bool:
        """Remove an acceptance criterion."""
        if criterion in self.acceptance_criteria:
            self.acceptance_criteria.remove(criterion)
            self.updated_at = datetime.utcnow()
            return True
        return False