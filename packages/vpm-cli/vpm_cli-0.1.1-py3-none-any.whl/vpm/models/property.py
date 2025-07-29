from sqlmodel import Field, Relationship
from vpm.models.base import BaseModel
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from vpm.models.elements import Element
    from vpm.models.documents import Document

class Home(BaseModel, table=True):
    """Model representing a home property."""
    address: str
    rooms: list["Room"] = Relationship(back_populates="home", cascade_delete=True)
    documents: list["Document"] = Relationship(back_populates="home", cascade_delete=True)

class Room(BaseModel, table=True):
    """Model representing a room in a home."""
    level: int = Field(default=0)
    home_id: UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    elements: list["Element"] = Relationship(back_populates="room", cascade_delete=True)
    