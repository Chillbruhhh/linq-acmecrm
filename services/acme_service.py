"""Mock AcmeCRM service for in-memory contact storage."""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from models.acme_models import AcmeContact, AcmeContactResponse


class AcmeService:
    """Mock service simulating AcmeCRM contact management."""
    
    # In-memory storage for contacts
    _contacts: Dict[str, Dict] = {}
    
    @classmethod
    def create_contact(cls, contact: AcmeContact) -> AcmeContactResponse:
        """
        Create a new contact in AcmeCRM.
        
        Args:
            contact: Contact data in AcmeCRM format
            
        Returns:
            AcmeContactResponse with created contact details
        """
        # Generate unique contact ID
        contact_id = f"acme_{str(uuid.uuid4())[:8]}"
        
        # Create contact record
        contact_record = {
            "acme_contact": contact,
            "acme_created_at": datetime.utcnow().isoformat() + "Z",
            "acme_status": "active"
        }
        
        # Store in memory
        cls._contacts[contact_id] = contact_record
        
        return AcmeContactResponse(
            acme_contact_id=contact_id,
            acme_contact=contact,
            acme_created_at=contact_record["acme_created_at"],
            acme_status=contact_record["acme_status"]
        )
    
    @classmethod
    def get_contact(cls, contact_id: str) -> Optional[AcmeContactResponse]:
        """
        Retrieve a contact by ID from AcmeCRM.
        
        Args:
            contact_id: Unique contact identifier
            
        Returns:
            AcmeContactResponse if found, None otherwise
        """
        if contact_id not in cls._contacts:
            return None
        
        contact_record = cls._contacts[contact_id]
        return AcmeContactResponse(
            acme_contact_id=contact_id,
            acme_contact=contact_record["acme_contact"],
            acme_created_at=contact_record["acme_created_at"],
            acme_status=contact_record["acme_status"]
        )
    
    @classmethod
    def get_all_contacts(cls) -> List[AcmeContactResponse]:
        """
        Retrieve all contacts from AcmeCRM.
        
        Returns:
            List of all contacts in AcmeCRM
        """
        contacts = []
        for contact_id, contact_record in cls._contacts.items():
            contacts.append(
                AcmeContactResponse(
                    acme_contact_id=contact_id,
                    acme_contact=contact_record["acme_contact"],
                    acme_created_at=contact_record["acme_created_at"],
                    acme_status=contact_record["acme_status"]
                )
            )
        return contacts
    
    @classmethod
    def update_contact_status(cls, contact_id: str, status: str) -> bool:
        """
        Update the status of a contact in AcmeCRM.
        
        Args:
            contact_id: Unique contact identifier
            status: New status value
            
        Returns:
            True if update successful, False if contact not found
        """
        if contact_id not in cls._contacts:
            return False
        
        cls._contacts[contact_id]["acme_status"] = status
        return True
    
    @classmethod
    def delete_contact(cls, contact_id: str) -> bool:
        """
        Delete a contact from AcmeCRM.
        
        Args:
            contact_id: Unique contact identifier
            
        Returns:
            True if deletion successful, False if contact not found
        """
        if contact_id not in cls._contacts:
            return False
        
        del cls._contacts[contact_id]
        return True
    
    @classmethod
    def get_storage_stats(cls) -> Dict[str, int]:
        """
        Get statistics about the in-memory storage.
        
        Returns:
            Dictionary with storage statistics
        """
        return {
            "total_contacts": len(cls._contacts),
            "active_contacts": sum(1 for c in cls._contacts.values() if c["acme_status"] == "active"),
            "inactive_contacts": sum(1 for c in cls._contacts.values() if c["acme_status"] != "active")
        }
    
    @classmethod
    def clear_storage(cls) -> None:
        """Clear all contacts from in-memory storage (for testing)."""
        cls._contacts.clear()
