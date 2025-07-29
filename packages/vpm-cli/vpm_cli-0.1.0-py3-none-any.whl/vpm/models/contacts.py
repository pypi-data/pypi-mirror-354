from sqlmodel import Field, Relationship
from vpm.models.base import BaseModel
from typing import Optional
from vpm.models.documents import Document
from pydantic import field_validator
from vpm.utils.helpers import validate_email, validate_phone, validate_url

class Contact(BaseModel, table=True):
    """Model representing a contact."""
    email: str = Field(unique=True, nullable=False)
    phone: Optional[str] = Field(default=None)
    company: Optional[str] = None
    street: Optional[str] = None
    postal_box: Optional[str] = None
    town: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    documents: Optional[Document] = Relationship(back_populates="contact", cascade_delete=True)
    
    @field_validator("email")
    def validate_email(cls, v):
        return validate_email(v)

    @field_validator("phone")
    def validate_phone(cls, v):
        return validate_phone(v)
    
    @field_validator("website")
    def validate_website(cls, v):
        return validate_url(v)