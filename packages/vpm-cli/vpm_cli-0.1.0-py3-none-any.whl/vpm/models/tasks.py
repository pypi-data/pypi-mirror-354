from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from pydantic import field_validator
from vpm.utils.helpers import validate_url
from vpm.models.picklist import TaskCategory, IntervalUnit, Currency

if TYPE_CHECKING:
    from vpm.models.elements import Element
    from vpm.models.parts import Part

class TaskType(BaseModel):
    """Base type for maintenance tasks."""
    task_category: str | None = Field(default=TaskCategory.MAINTENANCE, nullable=True)
    interval: int | None = None
    interval_unit: str | None = None
    url: str | None= Field(default=None, nullable=True)

    @field_validator("task_category")
    def validate_task_category(cls, v):
        if v not in TaskCategory:
            raise ValueError(f"Invalid task category: {v}")
        return v

    @field_validator("interval_unit")
    def validate_interval_unit(cls, v):
        if v not in IntervalUnit:
            raise ValueError(f"Invalid interval unit: {v}")
        return v
    
    @field_validator("url")
    def validate_url(cls, v):
        return validate_url(v)

class Task(TaskType, table=True):
    """Model representing a maintenance task."""
    element_id: UUID = Field(foreign_key="element.id")
    element: "Element" = Relationship(back_populates="tasks")
    date_due: datetime | None = Field(default=None, nullable=True)
    date_complete: datetime | None = Field(default=None, nullable=True)
    complete: bool = Field(default=False)
    cost_parts: Decimal | None = Field(default=None, nullable=True) 
    cost_labor: Decimal | None = Field(default=None, nullable=True)
    currency: str | None = Field(default=None, nullable=True)
    # Optional relationship to Parts (no cascade delete since Parts belong to Elements)
    parts: list["Part"] = Relationship(back_populates="task")

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in Currency:
            raise ValueError(f"Invalid currency: {v}")
        return v
