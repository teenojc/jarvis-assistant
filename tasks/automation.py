"""Task Automation Module"""

from loguru import logger
from config import TASK_CONFIG


class TaskAutomation:
    """Automate various tasks"""
    
    def __init__(self):
        """Initialize task automation"""
        logger.info("Initializing Task Automation...")
        self.tasks = {}
        logger.info("Task Automation initialized")
    
    def add_task(self, task_id, task_name, action, params=None):
        """Add a new task"""
        logger.info(f"Adding task: {task_id} - {task_name}")
        self.tasks[task_id] = {
            'name': task_name,
            'action': action,
            'params': params or {},
        }
        return True
    
    def execute_task(self, task_id):
        """Execute a task"""
        if task_id not in self.tasks:
            logger.warning(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        logger.info(f"Executing task: {task['name']}")
        
        try:
            # Execute the action
            result = task['action'](**task['params'])
            logger.info(f"Task executed successfully: {task_id}")
            return result
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return False
    
    def list_tasks(self):
        """List all tasks"""
        return list(self.tasks.keys())
    
    def remove_task(self, task_id):
        """Remove a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Task removed: {task_id}")
            return True
        return False