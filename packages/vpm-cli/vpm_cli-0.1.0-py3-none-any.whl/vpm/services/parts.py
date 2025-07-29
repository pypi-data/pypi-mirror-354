from typing import Optional
from sqlmodel import Session, select
from vpm.models.parts import Part, PartType
from vpm.database.config import engine
from vpm.services.base import BaseService

class PartService(BaseService[Part]):
    """Service for managing parts in the database."""
    def __init__(self):
        super().__init__(Part)