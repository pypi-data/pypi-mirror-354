"""Task management service implementation."""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
import json
from pathlib import Path

from ..models.task import Task, TaskStatus, TaskPriority, SubTask
from ..storage.task_storage import TaskStorage, TaskNotFoundError
from ..models.dependency_graph import DependencyGraph, CycleError, DependencyImpact
from .complexity_analyzer import ComplexityAnalyzer

class TaskValidationError(Exception):
    """Raised when task validation fails."""
    pass

class TaskService:
    """Service for managing tasks and their relationships."""

    def __init__(self, file_path: str = "tasks/tasks.json"):
        """Initialize task service.
        
        Args:
            file_path: Path to the tasks JSON file. Defaults to "tasks/tasks.json".
        """
        self.file_path = file_path
        self.storage = TaskStorage(file_path)
        self.dependency_graph = DependencyGraph()
        self.complexity_analyzer = ComplexityAnalyzer(self.dependency_graph)
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from JSON file and build dependency graph."""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                tasks = [Task(**task_data) for task_data in data.get('tasks', [])]
                
                # Clear and rebuild dependency graph
                self.dependency_graph = DependencyGraph()
                for task in tasks:
                    self.dependency_graph.add_task(task)
                
        except FileNotFoundError:
            # Create empty tasks file if it doesn't exist
            Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
            self._save_tasks([])
    
    def _save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to JSON file."""
        data = {'tasks': [task.dict() for task in tasks]}
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: Optional[List[int]] = None,
        details: Optional[str] = None,
        test_strategy: Optional[str] = None,
        
        sprint: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Task:
        """Create a new task.
        
        Args:
            title: Task title
            description: Task description
            priority: Task priority
            dependencies: List of task IDs this task depends on
            details: Detailed implementation notes
            test_strategy: Testing strategy
            
            sprint: Sprint identifier
            metadata: Additional metadata
            
        Returns:
            The created task.
            
        Raises:
            TaskValidationError: If task validation fails.
        """
        task_id = self.storage.get_next_task_id()
        
        # Validate dependencies
        if dependencies:
            completed_tasks = self.storage.get_completed_task_ids()
            for dep_id in dependencies:
                try:
                    self.storage.get_task(dep_id)
                except TaskNotFoundError:
                    raise TaskValidationError(f"Dependency task {dep_id} not found")

        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            dependencies=dependencies or [],
            details=details,
            test_strategy=test_strategy,
            
            sprint=sprint,
            metadata=metadata or {}
        )
        
        self.storage.save_task(task)
        return task

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            The task with the specified ID.
            
        Raises:
            TaskNotFoundError: If the task is not found.
        """
        return self.storage.get_task(task_id)

    def list_tasks(
        self,
        status_filter: Optional[TaskStatus] = None,
        priority_filter: Optional[TaskPriority] = None,
        sprint_filter: Optional[str] = None
    ) -> List[Task]:
        """List tasks with optional filters.
        
        Args:
            status_filter: Filter by task status
            priority_filter: Filter by task priority
            sprint_filter: Filter by sprint identifier
            
        Returns:
            List of tasks matching the filters.
        """
        tasks = self.storage.list_tasks(status_filter)
        
        if priority_filter:
            tasks = [t for t in tasks if t.priority == priority_filter]
            
        if sprint_filter:
            tasks = [t for t in tasks if t.sprint == sprint_filter]
            
        return tasks

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        dependencies: Optional[List[int]] = None,
        details: Optional[str] = None,
        test_strategy: Optional[str] = None,
        
        sprint: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Task:
        """Update a task.
        
        Args:
            task_id: ID of the task to update
            title: New title
            description: New description
            priority: New priority
            dependencies: New dependencies
            details: New implementation details
            test_strategy: New test strategy
            
            sprint: New sprint identifier
            metadata: New metadata
            
        Returns:
            The updated task.
            
        Raises:
            TaskNotFoundError: If the task is not found.
            TaskValidationError: If task validation fails.
        """
        task = self.storage.get_task(task_id)
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if dependencies is not None:
            # Validate dependencies
            for dep_id in dependencies:
                if dep_id == task_id:
                    raise TaskValidationError("Task cannot depend on itself")
                try:
                    self.storage.get_task(dep_id)
                except TaskNotFoundError:
                    raise TaskValidationError(f"Dependency task {dep_id} not found")
            task.dependencies = dependencies
        if details is not None:
            task.details = details
        if test_strategy is not None:
            task.test_strategy = test_strategy
        if sprint is not None:
            task.sprint = sprint
        if metadata is not None:
            task.metadata = metadata
            
        task.updated_at = datetime.utcnow()
        self.storage.save_task(task)
        return task

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        """Update a task's status.
        
        Args:
            task_id: ID of the task to update
            new_status: New status
            
        Returns:
            The updated task.
            
        Raises:
            TaskNotFoundError: If the task is not found.
            TaskValidationError: If the task is blocked by dependencies.
        """
        task = self.storage.get_task(task_id)
        
        if new_status == TaskStatus.DONE:
            # Check dependencies
            completed_tasks = self.storage.get_completed_task_ids()
            if task.is_blocked(completed_tasks):
                raise TaskValidationError("Cannot mark task as done: blocked by dependencies")
        
        task.update_status(new_status)
        self.storage.save_task(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete.
            
        Raises:
            TaskNotFoundError: If the task is not found.
            TaskValidationError: If other tasks depend on this task.
        """
        # Check if any other tasks depend on this one
        all_tasks = self.storage.list_tasks()
        dependent_tasks = [t for t in all_tasks if task_id in t.dependencies]
        
        if dependent_tasks:
            task_ids = ", ".join(str(t.id) for t in dependent_tasks)
            raise TaskValidationError(
                f"Cannot delete task {task_id}: other tasks depend on it: {task_ids}"
            )
            
        self.storage.delete_task(task_id)

    def expand_task(
        self,
        task_id: int,
        num_subtasks: int = 3,
        with_research: bool = False,
        context_prompt: Optional[str] = None
    ) -> Task:
        """Expand a task into subtasks.
        
        Args:
            task_id: ID of the task to expand
            num_subtasks: Number of subtasks to create
            with_research: Whether to use research-backed generation
            context_prompt: Additional context for subtask generation
            
        Returns:
            The expanded task.
            
        Raises:
            TaskNotFoundError: If the task is not found.
            NotImplementedError: If research-backed generation is requested.
        """
        if with_research:
            # TODO: Implement research-backed generation using Perplexity
            raise NotImplementedError("Research-backed generation not implemented yet")
            
        task = self.storage.get_task(task_id)
        
        # For now, just create placeholder subtasks
        for i in range(num_subtasks):
            task.add_subtask(
                title=f"Subtask {i+1}",
                description=f"Implementation details for subtask {i+1}"
            )
            
        self.storage.save_task(task)
        return task

    def get_next_task(self, min_priority: Optional[TaskPriority] = None) -> Optional[Task]:
        """Get the next task to work on.
        
        Args:
            min_priority: Minimum priority level to consider
            
        Returns:
            The next task to work on, or None if no eligible tasks found.
        """
        tasks = self.storage.list_tasks()
        completed_task_ids = self.storage.get_completed_task_ids()
        
        # Filter out completed and blocked tasks
        eligible_tasks = [
            t for t in tasks
            if t.status == TaskStatus.PENDING
            and not t.is_blocked(completed_task_ids)
            and (min_priority is None or t.priority.value >= min_priority.value)
        ]
        
        if not eligible_tasks:
            return None
            
        # Sort by priority (high to low) and ID (low to high)
        eligible_tasks.sort(key=lambda t: (-TaskPriority[t.priority.upper()].value, t.id))
        return eligible_tasks[0]

    def get_dependency_path(self, from_task: int, to_task: int) -> Optional[List[int]]:
        """Find the dependency path between two tasks.
        
        Args:
            from_task: Starting task ID
            to_task: Target task ID
            
        Returns:
            List of task IDs showing the dependency path, or None if no path exists.
            
        Raises:
            TaskNotFoundError: If either task doesn't exist.
        """
        self._validate_task_exists(from_task)
        self._validate_task_exists(to_task)
        return self.dependency_graph.get_dependency_path(from_task, to_task)

    def analyze_dependency_impact(self, task_id: int) -> DependencyImpact:
        """Analyze the impact of a task's dependencies.
        
        Args:
            task_id: ID of the task to analyze
            
        Returns:
            DependencyImpact object containing impact analysis.
            
        Raises:
            TaskNotFoundError: If the task doesn't exist.
        """
        self._validate_task_exists(task_id)
        return self.dependency_graph.analyze_dependency_impact(task_id)

    def get_dependent_tasks(self, task_id: int) -> List[Task]:
        """Get all tasks that depend on the given task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            List of tasks that depend on the given task.
            
        Raises:
            TaskNotFoundError: If the task doesn't exist.
        """
        self._validate_task_exists(task_id)
        dependent_ids = self.dependency_graph.get_dependent_tasks(task_id)
        return [self.get_task(dep_id) for dep_id in dependent_ids]

    def add_dependency(self, task_id: int, depends_on_id: int) -> None:
        """Add a dependency between tasks.
        
        Args:
            task_id: ID of the task that will depend on another
            depends_on_id: ID of the task that will become a dependency
            
        Raises:
            TaskNotFoundError: If either task doesn't exist
            CycleError: If adding the dependency would create a cycle
            TaskValidationError: If the dependency is invalid
        """
        self._validate_task_exists(task_id)
        self._validate_task_exists(depends_on_id)
        
        try:
            self.dependency_graph.add_dependency(task_id, depends_on_id)
            self._save_tasks()
        except CycleError as e:
            raise TaskValidationError(str(e))

    def remove_dependency(self, task_id: int, depends_on_id: int) -> None:
        """Remove a dependency between tasks.
        
        Args:
            task_id: ID of the task to remove dependency from
            depends_on_id: ID of the task to remove as a dependency
            
        Raises:
            TaskNotFoundError: If either task doesn't exist
        """
        self._validate_task_exists(task_id)
        self._validate_task_exists(depends_on_id)
        
        self.dependency_graph.remove_dependency(task_id, depends_on_id)
        self._save_tasks()

    def validate_dependencies(self) -> List[str]:
        """Validate all task dependencies.
        
        Returns:
            List of validation issues found.
        """
        return self.dependency_graph.validate_all_dependencies()

    def _validate_task_exists(self, task_id: int) -> None:
        """Validate that a task exists.
        
        Args:
            task_id: ID of the task to validate
            
        Raises:
            TaskNotFoundError: If the task doesn't exist
        """
        if task_id not in self.dependency_graph.tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")

    def add_subtask(
        self,
        task_id: Union[str, int],
        title: str,
        description: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ) -> SubTask:
        """Add a subtask to a task.
        
        Args:
            task_id: ID of the parent task
            title: Subtask title
            description: Optional subtask description
            dependencies: Optional list of subtask IDs this subtask depends on
            
        Returns:
            The created subtask.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
            TaskValidationError: If subtask validation fails.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        # Validate dependencies if provided
        if dependencies:
            for dep_id in dependencies:
                if not task.get_subtask(dep_id):
                    raise TaskValidationError(f"Dependency subtask {dep_id} not found")

        subtask = task.add_subtask(title, description, dependencies)
        self.storage.save_task(task)
        return subtask

    def remove_subtask(self, task_id: Union[str, int], subtask_id: str) -> bool:
        """Remove a subtask from a task.
        
        Args:
            task_id: ID of the parent task
            subtask_id: ID of the subtask to remove
            
        Returns:
            True if the subtask was removed, False otherwise.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        if task.remove_subtask(subtask_id):
            # Remove this subtask from other subtasks' dependencies
            for other_subtask in task.subtasks:
                if subtask_id in other_subtask.dependencies:
                    other_subtask.dependencies.remove(subtask_id)
            
            self.storage.save_task(task)
            return True
        return False

    def update_subtask_status(
        self,
        task_id: Union[str, int],
        subtask_id: str,
        new_status: TaskStatus
    ) -> Optional[SubTask]:
        """Update a subtask's status.
        
        Args:
            task_id: ID of the parent task
            subtask_id: ID of the subtask to update
            new_status: New status to set
            
        Returns:
            The updated subtask, or None if not found.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        subtask = task.get_subtask(subtask_id)
        if subtask:
            subtask.update_status(new_status)
            
            # If all subtasks are done, mark the parent task as done
            if (new_status == TaskStatus.DONE and 
                all(st.status == TaskStatus.DONE for st in task.subtasks)):
                task.update_status(TaskStatus.DONE)
            
            self.storage.save_task(task)
            return subtask
        return None

    def add_subtask_dependency(
        self,
        task_id: Union[str, int],
        subtask_id: str,
        depends_on_id: str
    ) -> bool:
        """Add a dependency between subtasks.
        
        Args:
            task_id: ID of the parent task
            subtask_id: ID of the subtask that will depend on another
            depends_on_id: ID of the subtask that will become a dependency
            
        Returns:
            True if the dependency was added, False otherwise.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
            TaskValidationError: If dependency validation fails.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        subtask = task.get_subtask(subtask_id)
        depends_on = task.get_subtask(depends_on_id)
        
        if not subtask or not depends_on:
            raise TaskValidationError("Both subtasks must exist")
            
        if subtask_id == depends_on_id:
            raise TaskValidationError("Subtask cannot depend on itself")
            
        # Check for circular dependencies
        def has_circular_dependency(current_id: str, target_id: str, visited: set) -> bool:
            if current_id == target_id:
                return True
            if current_id in visited:
                return False
            visited.add(current_id)
            current = task.get_subtask(current_id)
            return any(has_circular_dependency(dep, target_id, visited.copy()) 
                     for dep in current.dependencies)

        if has_circular_dependency(depends_on_id, subtask_id, set()):
            raise TaskValidationError("Adding this dependency would create a cycle")

        if depends_on_id not in subtask.dependencies:
            subtask.dependencies.append(depends_on_id)
            self.storage.save_task(task)
            return True
        return False

    def remove_subtask_dependency(
        self,
        task_id: Union[str, int],
        subtask_id: str,
        depends_on_id: str
    ) -> bool:
        """Remove a dependency between subtasks.
        
        Args:
            task_id: ID of the parent task
            subtask_id: ID of the subtask to remove dependency from
            depends_on_id: ID of the subtask to remove as a dependency
            
        Returns:
            True if the dependency was removed, False otherwise.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        subtask = task.get_subtask(subtask_id)
        if subtask and depends_on_id in subtask.dependencies:
            subtask.dependencies.remove(depends_on_id)
            self.storage.save_task(task)
            return True
        return False

    def get_subtask_dependencies(
        self,
        task_id: Union[str, int],
        subtask_id: str
    ) -> List[SubTask]:
        """Get all dependencies for a subtask.
        
        Args:
            task_id: ID of the parent task
            subtask_id: ID of the subtask
            
        Returns:
            List of subtasks that this subtask depends on.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        subtask = task.get_subtask(subtask_id)
        if subtask:
            return [task.get_subtask(dep_id) for dep_id in subtask.dependencies 
                   if task.get_subtask(dep_id)]
        return []

    def get_subtask_dependents(
        self,
        task_id: Union[str, int],
        subtask_id: str
    ) -> List[SubTask]:
        """Get all subtasks that depend on this subtask.
        
        Args:
            task_id: ID of the parent task
            subtask_id: ID of the subtask
            
        Returns:
            List of subtasks that depend on this subtask.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")

        return [st for st in task.subtasks if subtask_id in st.dependencies]

    def get_ready_subtasks(self, task_id: Union[str, int]) -> List[SubTask]:
        """Get all subtasks that are ready to be worked on.
        
        A subtask is ready if:
        1. It is not completed
        2. All its dependencies are completed
        
        Args:
            task_id: ID of the parent task
            
        Returns:
            List of subtasks ready to be worked on.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        return task.get_ready_subtasks()

    def get_blocked_subtasks(self, task_id: Union[str, int]) -> List[SubTask]:
        """Get all subtasks that are blocked by dependencies.
        
        Args:
            task_id: ID of the parent task
            
        Returns:
            List of blocked subtasks.
            
        Raises:
            TaskNotFoundError: If the parent task is not found.
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        return task.get_blocked_subtasks() 