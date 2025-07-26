"""Pydantic models for Linq contact format."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LinqContact(BaseModel):
    """Model representing contact data from Linq platform."""
    
    firstName: str = Field(..., description="Contact's first name", min_length=1, max_length=100)
    lastName: str = Field(..., description="Contact's last name", min_length=1, max_length=100)
    email: EmailStr = Field(..., description="Contact's email address")
    phone: Optional[str] = Field(None, description="Contact's phone number", max_length=20)
    company: Optional[str] = Field(None, description="Contact's company name", max_length=200)
    notes: Optional[str] = Field(None, description="Additional notes about the contact", max_length=1000)

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "company": "Tech Corp",
                "notes": "Met at networking event"
            }
        }


class LinqContactResponse(BaseModel):
    """Response model for Linq contact operations."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    contact_id: str = Field(..., description="Unique identifier for the contact in AcmeCRM")
    message: str = Field(..., description="Human-readable response message")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": True,
                "contact_id": "acme_12345",
                "message": "Contact successfully created in AcmeCRM"
            }
        }
