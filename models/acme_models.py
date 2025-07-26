"""Pydantic models for AcmeCRM contact format."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class AcmeContact(BaseModel):
    """Model representing contact data in AcmeCRM format."""
    
    acme_first_name: str = Field(..., description="Contact's first name", min_length=1, max_length=100)
    acme_last_name: str = Field(..., description="Contact's last name", min_length=1, max_length=100)
    acme_email: EmailStr = Field(..., description="Contact's email address")
    acme_phone_number: Optional[str] = Field(None, description="Contact's phone number", max_length=20)
    acme_company_name: Optional[str] = Field(None, description="Contact's company name", max_length=200)
    acme_notes: Optional[str] = Field(None, description="Additional notes about the contact", max_length=1000)

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "acme_first_name": "John",
                "acme_last_name": "Doe",
                "acme_email": "john.doe@example.com",
                "acme_phone_number": "+1-555-123-4567",
                "acme_company_name": "Tech Corp",
                "acme_notes": "Met at networking event"
            }
        }


class AcmeContactResponse(BaseModel):
    """Response model for AcmeCRM contact operations."""
    
    acme_contact_id: str = Field(..., description="Unique identifier for the contact in AcmeCRM")
    acme_contact: AcmeContact = Field(..., description="Contact data in AcmeCRM format")
    acme_created_at: str = Field(..., description="Timestamp when contact was created")
    acme_status: str = Field(..., description="Status of the contact in AcmeCRM")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "acme_contact_id": "acme_12345",
                "acme_contact": {
                    "acme_first_name": "John",
                    "acme_last_name": "Doe",
                    "acme_email": "john.doe@example.com",
                    "acme_phone_number": "+1-555-123-4567",
                    "acme_company_name": "Tech Corp",
                    "acme_notes": "Met at networking event"
                },
                "acme_created_at": "2025-07-25T10:30:00Z",
                "acme_status": "active"
            }
        }
