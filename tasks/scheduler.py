"""Task Scheduling Module"""

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from config import TASK_CONFIG


class TaskScheduler:
    """Schedule and manage recurring tasks"""
    
    def __init__(self):
        """Initialize task scheduler"""
        logger.info("Initializing Task Scheduler...")
        
        self.scheduler = BackgroundScheduler(timezone=TASK_CONFIG['timezone'])
        self.scheduled_tasks = {}
        
        logger.info("Task Scheduler initialized")
    
    def schedule_task(self, task_id, job_func, trigger='cron', **kwargs):
        """Schedule a task"""
        logger.info(f"Scheduling task: {task_id}")
        
        try:
            job = self.scheduler.add_job(
                job_func,
                trigger=trigger,
                id=task_id,
                **kwargs
            )
            
            self.scheduled_tasks[task_id] = job
            logger.info(f"Task scheduled: {task_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error scheduling task: {e}")
            return False
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Task Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Task Scheduler stopped")
    
    def list_scheduled_tasks(self):
        """List all scheduled tasks"""
        return list(self.scheduled_tasks.keys())
    
    def remove_scheduled_task(self, task_id):
        """Remove a scheduled task"""
        if task_id in self.scheduled_tasks:
            self.scheduler.remove_job(task_id)
            del self.scheduled_tasks[task_id]
            logger.info(f"Scheduled task removed: {task_id}")
            return True
        return False