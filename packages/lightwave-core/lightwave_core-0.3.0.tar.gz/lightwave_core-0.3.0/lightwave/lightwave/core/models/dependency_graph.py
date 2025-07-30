from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
from enum import Enum
from datetime import datetime

from pydantic import BaseModel

from .task import Task, TaskStatus


class CycleError(Exception):
    """Raised when a circular dependency is detected."""
    pass


class DependencyImpact(BaseModel):
    """Model for dependency impact analysis results."""
    affected_tasks: List[int]
    blocked_tasks: List[int]
    completion_blockers: List[int]
    risk_level: str
    impact_description: str


class DependencyGraph(BaseModel):
    """Graph-based task dependency management system."""
    
    # Store tasks by their IDs for quick lookup
    tasks: Dict[int, Task] = {}
    
    # Adjacency lists for dependencies (task_id -> list of dependency_ids)
    dependencies: Dict[int, List[int]] = defaultdict(list)
    
    # Reverse dependencies for efficient ancestor lookup
    reverse_dependencies: Dict[int, List[int]] = defaultdict(list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the graph."""
        self.tasks[task.id] = task
        self.dependencies[task.id] = task.dependencies
        for dep_id in task.dependencies:
            self.reverse_dependencies[dep_id].append(task.id)
    
    def remove_task(self, task_id: int) -> None:
        """Remove a task from the graph."""
        if task_id in self.tasks:
            # Remove from dependencies
            deps = self.dependencies.pop(task_id, [])
            for dep_id in deps:
                if dep_id in self.reverse_dependencies:
                    self.reverse_dependencies[dep_id].remove(task_id)
            
            # Remove from reverse dependencies
            rev_deps = self.reverse_dependencies.pop(task_id, [])
            for rev_dep_id in rev_deps:
                if rev_dep_id in self.dependencies:
                    self.dependencies[rev_dep_id].remove(task_id)
            
            # Remove the task
            self.tasks.pop(task_id)
    
    def add_dependency(self, task_id: int, depends_on_id: int) -> None:
        """Add a dependency between tasks."""
        if task_id not in self.tasks or depends_on_id not in self.tasks:
            raise ValueError("Both tasks must exist in the graph")
        
        if task_id == depends_on_id:
            raise CycleError("Task cannot depend on itself")
        
        # Check for circular dependencies
        if self._would_create_cycle(task_id, depends_on_id):
            cycle_path = self._find_cycle_path(task_id, depends_on_id)
            cycle_str = " -> ".join(str(t) for t in cycle_path)
            raise CycleError(f"Adding this dependency would create a cycle: {cycle_str}")
        
        if depends_on_id not in self.dependencies[task_id]:
            self.dependencies[task_id].append(depends_on_id)
            self.reverse_dependencies[depends_on_id].append(task_id)
            self.tasks[task_id].dependencies.append(depends_on_id)
    
    def remove_dependency(self, task_id: int, depends_on_id: int) -> None:
        """Remove a dependency between tasks."""
        if task_id in self.dependencies and depends_on_id in self.dependencies[task_id]:
            self.dependencies[task_id].remove(depends_on_id)
            self.reverse_dependencies[depends_on_id].remove(task_id)
            self.tasks[task_id].dependencies.remove(depends_on_id)
    
    def get_blocked_tasks(self) -> List[int]:
        """Get IDs of tasks that are blocked by incomplete dependencies."""
        blocked = []
        completed_ids = {t.id for t in self.tasks.values() if t.status == TaskStatus.DONE}
        
        for task_id, deps in self.dependencies.items():
            if any(dep_id not in completed_ids for dep_id in deps):
                blocked.append(task_id)
        
        return blocked
    
    def get_available_tasks(self) -> List[int]:
        """Get IDs of tasks that are ready to be worked on (all dependencies satisfied)."""
        completed_ids = {t.id for t in self.tasks.values() if t.status == TaskStatus.DONE}
        pending_ids = {t.id for t in self.tasks.values() if t.status != TaskStatus.DONE}
        
        return [
            task_id for task_id in pending_ids
            if all(dep_id in completed_ids for dep_id in self.dependencies[task_id])
        ]
    
    def get_dependent_tasks(self, task_id: int) -> List[int]:
        """Get IDs of tasks that depend on the given task."""
        return self.reverse_dependencies.get(task_id, [])
    
    def get_dependency_path(self, from_task: int, to_task: int) -> Optional[List[int]]:
        """Find the dependency path between two tasks if it exists."""
        if from_task not in self.tasks or to_task not in self.tasks:
            return None
            
        visited = set()
        path = []
        
        def dfs(current: int) -> bool:
            if current == to_task:
                path.append(current)
                return True
                
            if current in visited:
                return False
                
            visited.add(current)
            path.append(current)
            
            for dep in self.dependencies[current]:
                if dfs(dep):
                    return True
                    
            path.pop()
            return False
            
        if dfs(from_task):
            return path
        return None
    
    def analyze_dependency_impact(self, task_id: int) -> DependencyImpact:
        """Analyze the impact of a task's dependencies on the project."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        # Find all tasks affected by this task
        affected = set()
        queue = [task_id]
        while queue:
            current = queue.pop(0)
            for dependent in self.reverse_dependencies[current]:
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)
                    
        # Find tasks blocking this task
        blockers = set()
        queue = [task_id]
        while queue:
            current = queue.pop(0)
            for dep in self.dependencies[current]:
                if self.tasks[dep].status != TaskStatus.DONE:
                    blockers.add(dep)
                    queue.append(dep)
                    
        # Calculate risk level
        risk_level = "low"
        if len(affected) > 5:
            risk_level = "high"
        elif len(affected) > 2:
            risk_level = "medium"
            
        # Generate impact description
        impact_desc = []
        if affected:
            impact_desc.append(f"Affects {len(affected)} other tasks")
        if blockers:
            impact_desc.append(f"Blocked by {len(blockers)} incomplete tasks")
            
        return DependencyImpact(
            affected_tasks=list(affected),
            blocked_tasks=list(blockers),
            completion_blockers=[b for b in blockers if self.tasks[b].status != TaskStatus.DONE],
            risk_level=risk_level,
            impact_description=", ".join(impact_desc) or "No significant impact"
        )
    
    def validate_all_dependencies(self) -> List[str]:
        """Validate all dependencies in the graph and return a list of issues."""
        issues = []
        
        # Check for missing tasks
        all_deps = {dep for deps in self.dependencies.values() for dep in deps}
        for dep_id in all_deps:
            if dep_id not in self.tasks:
                issues.append(f"Task {dep_id} is referenced as a dependency but does not exist")
        
        # Check for cycles
        try:
            cycles = self._find_all_cycles()
            for cycle in cycles:
                cycle_str = " -> ".join(str(t) for t in cycle)
                issues.append(f"Circular dependency detected: {cycle_str}")
        except CycleError as e:
            issues.append(str(e))
            
        # Check for redundant dependencies
        for task_id, deps in self.dependencies.items():
            direct_deps = set(deps)
            indirect_deps = set()
            for dep in deps:
                path = self.get_dependency_path(task_id, dep)
                if path and len(path) > 2:  # Path length > 2 means there's an indirect path
                    indirect_deps.add(dep)
            if indirect_deps:
                deps_str = ", ".join(str(d) for d in indirect_deps)
                issues.append(f"Task {task_id} has redundant dependencies that could be removed: {deps_str}")
        
        return issues
    
    def _would_create_cycle(self, task_id: int, new_dep_id: int) -> bool:
        """Check if adding a dependency would create a cycle."""
        visited = set()
        path = []
        
        def dfs(current_id: int) -> bool:
            if current_id == task_id:
                path.append(current_id)
                return True
            if current_id in visited:
                return False
            
            visited.add(current_id)
            path.append(current_id)
            
            for dep_id in self.dependencies[current_id]:
                if dfs(dep_id):
                    return True
                    
            path.pop()
            return False
        
        return dfs(new_dep_id)
    
    def _find_cycle_path(self, task_id: int, new_dep_id: int) -> List[int]:
        """Find the path that would create a cycle when adding a new dependency."""
        visited = set()
        path = []
        
        def dfs(current_id: int) -> bool:
            if current_id == task_id:
                path.append(current_id)
                return True
            if current_id in visited:
                return False
            
            visited.add(current_id)
            path.append(current_id)
            
            for dep_id in self.dependencies[current_id]:
                if dfs(dep_id):
                    return True
                    
            path.pop()
            return False
        
        if dfs(new_dep_id):
            return [task_id] + path
        return []
    
    def _find_all_cycles(self) -> List[List[int]]:
        """Find all cycles in the dependency graph."""
        cycles = []
        visited = set()
        path = []
        
        def dfs(task_id: int) -> None:
            if task_id in path:
                cycle = path[path.index(task_id):] + [task_id]
                cycles.append(cycle)
                return
                
            if task_id in visited:
                return
                
            visited.add(task_id)
            path.append(task_id)
            
            for dep_id in self.dependencies[task_id]:
                dfs(dep_id)
                
            path.pop()
            
        for task_id in self.tasks:
            if task_id not in visited:
                dfs(task_id)
                
        return cycles 