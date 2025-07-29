from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from pydantic import field_validator
from vpm.utils.helpers import validate_url
from vpm.models.picklist import Currency


if TYPE_CHECKING:
    from vpm.models.tasks import Task
    from vpm.models.parts import Part
    from vpm.models.documents import Document
    from vpm.models.property import Room

class ElementType(BaseModel):
    """Base type for equipment elements."""
    brand: str | None = Field(default=None, nullable=True)
    model: str | None = Field(default=None, nullable=True)
    model_number: int | None = Field(default=None, nullable=True)
    manual_url: str | None = Field(default=None, nullable=True)
    manufacture_url: str | None = None
    cost: Decimal | None = Field(decimal_places=2, default=None, nullable=True)
    currency: str | None = Field(default="USD")

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in Currency:
            raise ValueError(f"Invalid currency: {v}")
        return v
    
    @field_validator("manual_url")
    def validate_manual_url(cls, v):
        return validate_url(v)
    
    @field_validator("manufacture_url")
    def validate_manufacture_url(cls, v):
        return validate_url(v)

class Element(ElementType, table=True):
    """Model representing an equipment element."""
    serial_num: str | None = Field(default=None, nullable=True)
    install_date: datetime | None = Field(default=None, nullable=True)
    remove_date: datetime | None = Field(default=None, nullable=True)
    room_id: UUID = Field(foreign_key="room.id")
    room: "Room" = Relationship(back_populates="elements")
    tasks: list["Task"] = Relationship(back_populates="element", cascade_delete=True)
    parts: list["Part"] = Relationship(back_populates="element", cascade_delete=True)
    documents: list["Document"] = Relationship(back_populates="element", cascade_delete=True)
 