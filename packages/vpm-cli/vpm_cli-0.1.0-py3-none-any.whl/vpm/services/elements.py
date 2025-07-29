from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import Session, select
from vpm.database import engine
from vpm.models.elements import Element
from vpm.models.tasks import Task
from vpm.services.base import BaseService
from vpm.utils.helpers import utc_now

class ElementService(BaseService[Element]):
    """Service for managing equipment elements."""
    
    def __init__(self):
        super().__init__(Element)
    
    def get_active_elements(self) -> List[Element]:
        """Get all active elements (not removed)."""
        with Session(engine) as session:
            return session.exec(
                select(Element).where(Element.remove_date.is_(None))
            ).all()

class TaskService(BaseService[Task]):
    """Service for managing maintenance tasks."""
    
    def __init__(self):
        super().__init__(Task)
    
    def get_due_tasks(self) -> List[Task]:
        """Get all tasks that are due."""
        now = utc_now()
        with Session(engine) as session:
            return session.exec(
                select(Task)
                .where(Task.date_due <= now)
                .where(Task.complete == False)
            ).all()
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        with Session(engine) as session:
            return session.exec(
                select(Task).where(Task.complete == True)
            ).all()
    
    def complete_task(self, task_id: UUID) -> Optional[Task]:
        """Mark a task as complete."""
        return self.update(
            task_id,
            complete=True,
            date_complete=utc_now()
        ) 