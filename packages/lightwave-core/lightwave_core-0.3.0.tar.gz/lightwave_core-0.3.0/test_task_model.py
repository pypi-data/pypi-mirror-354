"""Tests for the Task model."""

import pytest
from datetime import datetime
from uuid import uuid4

from lightwave.core.models.task import Task, TaskStatus, TaskPriority, SubTask


class TestTaskModel:
    """Tests for the Task model functionality."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(
            id=1,
            title="Test Task",
            description="A test task for validation"
        )
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "A test task for validation"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM
        assert task.dependencies == []
        assert task.subtasks == []
    
    def test_task_with_all_fields(self):
        """Test task creation with all fields."""
        now = datetime.utcnow()
        task = Task(
            id=2,
            title="Complex Task",
            description="A complex task with all fields",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            sprint="sprint-1",
            assigned_to="john.doe@example.com",
            dependencies=[1],
            details="Detailed implementation notes",
            test_strategy="Unit and integration tests",
            estimated_hours=8.5,
            due_date=now,
            created_at=now
        )
        
        assert task.id == 2
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.priority == TaskPriority.HIGH
        assert task.sprint == "sprint-1"
        assert task.assigned_to == "john.doe@example.com"
        assert task.dependencies == [1]
        assert task.details == "Detailed implementation notes"
        assert task.test_strategy == "Unit and integration tests"
        assert task.estimated_hours == 8.5
        assert task.due_date == now
        assert task.created_at == now
    
    def test_task_status_update(self):
        """Test task status updates."""
        task = Task(id=3, title="Status Test", description="Test status updates")
        
        # Check initial status
        assert task.status == TaskStatus.PENDING
        
        # Update status
        task.update_status(TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at is not None
    
    def test_task_blocked_status(self):
        """Test task blocked status checking."""
        task = Task(
            id=4,
            title="Blocked Task",
            description="Task with dependencies",
            dependencies=[1, 2, 3]
        )
        
        # Task should be blocked when dependencies not completed
        assert task.is_blocked([]) is True
        assert task.is_blocked([1]) is True
        assert task.is_blocked([1, 2]) is True
        
        # Task should not be blocked when all dependencies completed
        assert task.is_blocked([1, 2, 3]) is False
        assert task.is_blocked([1, 2, 3, 4, 5]) is False
    
    def test_task_can_start(self):
        """Test task can start checking."""
        task = Task(
            id=5,
            title="Dependent Task",
            description="Task that depends on others",
            dependencies=[1, 2]
        )
        
        # Can't start if dependencies not completed
        assert task.can_start([]) is False
        assert task.can_start([1]) is False
        
        # Can start if all dependencies completed
        assert task.can_start([1, 2]) is True
        
        # Can't start if already in progress
        task.status = TaskStatus.IN_PROGRESS
        assert task.can_start([1, 2]) is False


class TestSubTaskModel:
    """Tests for the SubTask model functionality."""
    
    def test_subtask_creation(self):
        """Test basic subtask creation."""
        subtask = SubTask(
            title="Test Subtask",
            description="A test subtask"
        )
        
        assert subtask.title == "Test Subtask"
        assert subtask.description == "A test subtask"
        assert subtask.status == TaskStatus.PENDING
        assert subtask.dependencies == []
        assert len(subtask.id) > 0  # UUID generated
    
    def test_subtask_with_dependencies(self):
        """Test subtask with dependencies."""
        subtask_id_1 = str(uuid4())
        subtask_id_2 = str(uuid4())
        
        subtask = SubTask(
            title="Dependent Subtask",
            description="Subtask with dependencies",
            dependencies=[subtask_id_1, subtask_id_2]
        )
        
        assert subtask.dependencies == [subtask_id_1, subtask_id_2]
    
    def test_subtask_status_update(self):
        """Test subtask status updates."""
        subtask = SubTask(title="Status Test", description="Test status")
        
        # Check initial status
        assert subtask.status == TaskStatus.PENDING
        
        # Update status
        subtask.update_status(TaskStatus.DONE)
        assert subtask.status == TaskStatus.DONE
        assert subtask.updated_at is not None
    
    def test_subtask_blocked_status(self):
        """Test subtask blocked status."""
        dep_id_1 = str(uuid4())
        dep_id_2 = str(uuid4())
        
        subtask = SubTask(
            title="Blocked Subtask",
            dependencies=[dep_id_1, dep_id_2]
        )
        
        # Should be blocked when dependencies not completed
        assert subtask.is_blocked([]) is True
        assert subtask.is_blocked([dep_id_1]) is True
        
        # Should not be blocked when all dependencies completed
        assert subtask.is_blocked([dep_id_1, dep_id_2]) is False


class TestTaskWithSubtasks:
    """Tests for Task and SubTask integration."""
    
    def test_add_subtask(self):
        """Test adding subtasks to a task."""
        task = Task(id=6, title="Parent Task", description="Task with subtasks")
        
        # Add subtasks
        subtask1 = task.add_subtask("Subtask 1", "First subtask")
        subtask2 = task.add_subtask("Subtask 2", "Second subtask")
        
        assert len(task.subtasks) == 2
        assert task.subtasks[0] == subtask1
        assert task.subtasks[1] == subtask2
        assert subtask1.title == "Subtask 1"
        assert subtask2.title == "Subtask 2"
    
    def test_get_subtask(self):
        """Test retrieving subtasks by ID."""
        task = Task(id=7, title="Search Task", description="Task for searching subtasks")
        
        subtask = task.add_subtask("Findable Subtask", "Can be found")
        subtask_id = subtask.id
        
        # Should find the subtask
        found = task.get_subtask(subtask_id)
        assert found is not None
        assert found.id == subtask_id
        assert found.title == "Findable Subtask"
        
        # Should not find non-existent subtask
        assert task.get_subtask("non-existent-id") is None
    
    def test_remove_subtask(self):
        """Test removing subtasks."""
        task = Task(id=8, title="Remove Task", description="Task for removing subtasks")
        
        subtask1 = task.add_subtask("Keep This", "This stays")
        subtask2 = task.add_subtask("Remove This", "This goes")
        
        assert len(task.subtasks) == 2
        
        # Remove subtask
        removed = task.remove_subtask(subtask2.id)
        assert removed is True
        assert len(task.subtasks) == 1
        assert task.subtasks[0].id == subtask1.id
        
        # Try to remove non-existent subtask
        removed = task.remove_subtask("non-existent-id")
        assert removed is False
        assert len(task.subtasks) == 1
    
    def test_get_ready_subtasks(self):
        """Test getting ready-to-work subtasks."""
        task = Task(id=9, title="Ready Task", description="Task with ready subtasks")
        
        # Add subtasks with dependencies
        subtask1 = task.add_subtask("Independent", "No dependencies")
        subtask2 = task.add_subtask("Dependent", "Has dependencies", [subtask1.id])
        subtask3 = task.add_subtask("Also Independent", "No dependencies")
        
        # Initially, only independent subtasks should be ready
        ready = task.get_ready_subtasks()
        ready_ids = [st.id for st in ready]
        assert subtask1.id in ready_ids
        assert subtask3.id in ready_ids
        assert subtask2.id not in ready_ids
        
        # Complete first subtask
        subtask1.update_status(TaskStatus.DONE)
        
        # Now dependent subtask should also be ready
        ready = task.get_ready_subtasks()
        ready_ids = [st.id for st in ready]
        assert subtask2.id in ready_ids
        assert subtask3.id in ready_ids
        assert subtask1.id not in ready_ids  # Done tasks not "ready"
    
    def test_get_completion_percentage(self):
        """Test task completion percentage calculation."""
        task = Task(id=10, title="Progress Task", description="Task for progress tracking")
        
        # Task with no subtasks
        assert task.get_completion_percentage() == 0.0
        
        # Add subtasks
        subtask1 = task.add_subtask("Task 1")
        subtask2 = task.add_subtask("Task 2")
        subtask3 = task.add_subtask("Task 3")
        subtask4 = task.add_subtask("Task 4")
        
        # 0% complete
        assert task.get_completion_percentage() == 0.0
        
        # Complete 2 out of 4 subtasks
        subtask1.update_status(TaskStatus.DONE)
        subtask2.update_status(TaskStatus.DONE)
        
        assert task.get_completion_percentage() == 50.0
        
        # Complete all subtasks
        subtask3.update_status(TaskStatus.DONE)
        subtask4.update_status(TaskStatus.DONE)
        
        assert task.get_completion_percentage() == 100.0
    
    def test_acceptance_criteria(self):
        """Test acceptance criteria management."""
        task = Task(id=11, title="Criteria Task", description="Task with acceptance criteria")
        
        # Add acceptance criteria
        task.add_acceptance_criterion("Must have unit tests")
        task.add_acceptance_criterion("Must pass code review")
        task.add_acceptance_criterion("Must have documentation")
        
        assert len(task.acceptance_criteria) == 3
        assert "Must have unit tests" in task.acceptance_criteria
        assert "Must pass code review" in task.acceptance_criteria
        assert "Must have documentation" in task.acceptance_criteria
        
        # Remove acceptance criterion
        removed = task.remove_acceptance_criterion("Must pass code review")
        assert removed is True
        assert len(task.acceptance_criteria) == 2
        assert "Must pass code review" not in task.acceptance_criteria
        
        # Try to remove non-existent criterion
        removed = task.remove_acceptance_criterion("Non-existent criterion")
        assert removed is False
        assert len(task.acceptance_criteria) == 2


class TestTaskPriority:
    """Tests for TaskPriority enumeration."""
    
    def test_priority_values(self):
        """Test priority enum values."""
        assert TaskPriority.LOW == "low"
        assert TaskPriority.MEDIUM == "medium"
        assert TaskPriority.HIGH == "high"
        assert TaskPriority.CRITICAL == "critical"
    
    def test_priority_comparison(self):
        """Test priority comparison."""
        assert TaskPriority.LOW < TaskPriority.MEDIUM
        assert TaskPriority.MEDIUM < TaskPriority.HIGH
        assert TaskPriority.HIGH < TaskPriority.CRITICAL
        
        assert TaskPriority.CRITICAL > TaskPriority.HIGH
        assert TaskPriority.HIGH > TaskPriority.MEDIUM
        assert TaskPriority.MEDIUM > TaskPriority.LOW


class TestTaskStatus:
    """Tests for TaskStatus enumeration."""
    
    def test_status_values(self):
        """Test status enum values."""
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.IN_PROGRESS == "in_progress"
        assert TaskStatus.BLOCKED == "blocked"
        assert TaskStatus.CODE_REVIEW == "code_review"
        assert TaskStatus.TESTING == "testing"
        assert TaskStatus.DONE == "done"
        assert TaskStatus.CANCELLED == "cancelled"