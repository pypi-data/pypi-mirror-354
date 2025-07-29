from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from vpm.database import engine
from vpm.models.property import Home, Room
from vpm.services.base import BaseService

class HomeService(BaseService[Home]):
    """Service for managing homes."""
    
    def __init__(self):
        super().__init__(Home)

    def get(self) -> Home:
        """Get a home by name."""
        with Session(engine) as session:
            return session.exec(
                select(Home)).first()
    
class RoomService(BaseService[Room]):
    """Service for managing rooms."""
    
    def __init__(self):
        super().__init__(Room)
    