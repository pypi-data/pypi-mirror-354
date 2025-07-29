from typing import TypeVar, Generic, Type, Optional, List
from uuid import UUID
from sqlmodel import Session, select
from vpm.database import engine as default_engine
from vpm.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):
    """Base service class with common CRUD operations."""
    
    def __init__(self, model_class: Type[T], engine=None):
        self.model_class = model_class
        self.engine = engine or default_engine  # Use provided engine or fall back to default
    
    def create(self, item: T) -> T:
        """Create a new item."""
        with Session(self.engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
    
    def get_by_id(self, item_id: UUID) -> Optional[T]:
        """Get item by ID."""
        with Session(self.engine) as session:
            try:
                return session.exec(
                    select(self.model_class).where(self.model_class.id == item_id)
                ).first()
            except Exception as e:
                print(e)
                return None
    
    def get_by_name(self, name: str) -> Optional[T]:
        """Get item by name."""
        with Session(self.engine) as session:
            try:
                return session.exec(
                    select(self.model_class).where(self.model_class.name == name)
                ).first()
            except Exception as e:
                raise e
    
    def get_all(self) -> List[T]:
        """Get all items."""
        with Session(self.engine) as session:
            try:
                return session.exec(select(self.model_class)).all()
            except Exception as e:
                raise e
    
    def update(self, item_id: UUID, **kwargs) -> Optional[T]:
        """Update an item."""
        with Session(self.engine) as session:
            try:
                item = self.get_by_id(item_id)
                if item:
                    for key, value in kwargs.items():
                        setattr(item, key, value)
                    session.add(item)
                    session.commit()
                    session.refresh(item)
                    return item
            except Exception as e:
                raise e
            return item
    
    def delete(self, item_id: UUID) -> bool:
        """Delete an item."""
        with Session(self.engine) as session:
            item = self.get_by_id(item_id)
            if item:
                try:
                    session.delete(item)
                    session.commit()
                    return True
                except Exception as e:
                    raise e
            return False 