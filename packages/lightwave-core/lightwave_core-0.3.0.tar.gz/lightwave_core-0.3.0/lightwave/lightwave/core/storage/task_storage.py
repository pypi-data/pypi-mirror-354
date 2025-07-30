"""Task storage implementation using JSON files."""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from ..models.task import Task, TaskStatus

class TaskStorageError(Exception):
    """Base class for task storage errors."""
    pass

class TaskNotFoundError(TaskStorageError):
    """Raised when a task is not found."""
    pass

class TaskStorage:
    """Handles storage and retrieval of tasks using JSON files."""

    def __init__(self, file_path: str = "tasks/tasks.json"):
        """Initialize task storage.
        
        Args:
            file_path: Path to the tasks JSON file. Defaults to "tasks/tasks.json".
        """
        self.file_path = Path(file_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage file and directory exist."""
        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True)
        if not self.file_path.exists():
            self._save_tasks({})

    def _load_tasks(self) -> Dict[int, Dict[str, Any]]:
        """Load tasks from the JSON file."""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise TaskStorageError("Invalid JSON in tasks file")
        except FileNotFoundError:
            return {}

    def _save_tasks(self, tasks: Dict[int, Dict[str, Any]]) -> None:
        """Save tasks to the JSON file."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(tasks, f, indent=2)
        except (OSError, json.JSONEncodeError) as e:
            raise TaskStorageError(f"Failed to save tasks: {str(e)}")

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            The task with the specified ID.
            
        Raises:
            TaskNotFoundError: If the task is not found.
        """
        tasks = self._load_tasks()
        if str(task_id) not in tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return Task.from_dict(tasks[str(task_id)])

    def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        """List all tasks, optionally filtered by status.
        
        Args:
            status_filter: Optional status to filter tasks by.
            
        Returns:
            List of tasks matching the filter.
        """
        tasks = self._load_tasks()
        task_list = [Task.from_dict(task_data) for task_data in tasks.values()]
        
        if status_filter:
            task_list = [t for t in task_list if t.status == status_filter]
            
        return sorted(task_list, key=lambda t: t.id)

    def save_task(self, task: Task) -> None:
        """Save a task to storage.
        
        Args:
            task: The task to save.
        """
        tasks = self._load_tasks()
        tasks[str(task.id)] = task.to_dict()
        self._save_tasks(tasks)

    def delete_task(self, task_id: int) -> None:
        """Delete a task from storage.
        
        Args:
            task_id: The ID of the task to delete.
            
        Raises:
            TaskNotFoundError: If the task is not found.
        """
        tasks = self._load_tasks()
        if str(task_id) not in tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        del tasks[str(task_id)]
        self._save_tasks(tasks)

    def get_next_task_id(self) -> int:
        """Get the next available task ID.
        
        Returns:
            The next available task ID.
        """
        tasks = self._load_tasks()
        if not tasks:
            return 1
        return max(int(task_id) for task_id in tasks.keys()) + 1

    def get_completed_task_ids(self) -> List[int]:
        """Get IDs of all completed tasks.
        
        Returns:
            List of completed task IDs.
        """
        tasks = self._load_tasks()
        return [
            int(task_id)
            for task_id, task_data in tasks.items()
            if task_data.get("status") == TaskStatus.DONE.value
        ] 