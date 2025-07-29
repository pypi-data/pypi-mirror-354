from sqlmodel import Field, Relationship
from vpm.models.base import BaseModel
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from pydantic import field_validator
from vpm.models.picklist import Currency

if TYPE_CHECKING:
    from vpm.models.tasks import Task
    from vpm.models.elements import Element

class PartType(BaseModel):
    """Base type for parts."""
    brand: str|None = Field(default=None, nullable=True)
    model: str | None = Field(default=None)
    model_number: str | None = Field(default=None)
    cost: Decimal | None = Field(default=None)
    currency: str | None = Field(default=None)

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in Currency:
            raise ValueError(f"Invalid currency: {v}")
        return v

class Part(PartType, table=True):
    """Model representing a part."""
    serial_num: str | None = Field(default=None)
    install_date: datetime | None = Field(default=None)
    remove_date: datetime | None = Field(default=None)
    # Primary relationship to Element
    element_id: UUID = Field(foreign_key="element.id", nullable=False)
    element: "Element" = Relationship(back_populates="parts")
    # Optional relationship to Task
    task_id: UUID | None = Field(foreign_key="task.id", nullable=True)
    task: "Task" = Relationship(back_populates="parts")