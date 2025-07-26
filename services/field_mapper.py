"""Field mapping service for translating between Linq and AcmeCRM formats."""

from typing import Dict, Any
from models.linq_models import LinqContact
from models.acme_models import AcmeContact


class FieldMapper:
    """Service for mapping fields between Linq and AcmeCRM formats."""
    
    # Mapping from Linq fields to AcmeCRM fields
    LINQ_TO_ACME_MAPPING = {
        "firstName": "acme_first_name",
        "lastName": "acme_last_name",
        "email": "acme_email",
        "phone": "acme_phone_number",
        "company": "acme_company_name",
        "notes": "acme_notes"
    }
    
    # Reverse mapping from AcmeCRM fields to Linq fields
    ACME_TO_LINQ_MAPPING = {
        "acme_first_name": "firstName",
        "acme_last_name": "lastName",
        "acme_email": "email",
        "acme_phone_number": "phone",
        "acme_company_name": "company",
        "acme_notes": "notes"
    }
    
    @classmethod
    def map_linq_to_acme(cls, linq_contact: LinqContact) -> AcmeContact:
        """
        Map contact data from Linq format to AcmeCRM format.
        
        Args:
            linq_contact: Contact data in Linq format
            
        Returns:
            Contact data in AcmeCRM format
        """
        linq_dict = linq_contact.model_dump()
        acme_dict = {}
        
        for linq_field, acme_field in cls.LINQ_TO_ACME_MAPPING.items():
            if linq_field in linq_dict:
                acme_dict[acme_field] = linq_dict[linq_field]
        
        return AcmeContact(**acme_dict)
    
    @classmethod
    def map_acme_to_linq(cls, acme_contact: AcmeContact) -> LinqContact:
        """
        Map contact data from AcmeCRM format to Linq format.
        
        Args:
            acme_contact: Contact data in AcmeCRM format
            
        Returns:
            Contact data in Linq format
        """
        acme_dict = acme_contact.model_dump()
        linq_dict = {}
        
        for acme_field, linq_field in cls.ACME_TO_LINQ_MAPPING.items():
            if acme_field in acme_dict:
                linq_dict[linq_field] = acme_dict[acme_field]
        
        return LinqContact(**linq_dict)
    
    @classmethod
    def get_mapping_schema(cls) -> Dict[str, Any]:
        """
        Get the field mapping schema for documentation purposes.
        
        Returns:
            Dictionary containing both forward and reverse mappings
        """
        return {
            "linq_to_acme": cls.LINQ_TO_ACME_MAPPING,
            "acme_to_linq": cls.ACME_TO_LINQ_MAPPING,
            "description": "Field mapping between Linq and AcmeCRM contact formats"
        }
    
    @classmethod
    def validate_field_mapping(cls) -> bool:
        """
        Validate that the field mappings are consistent and bidirectional.
        
        Returns:
            True if mappings are valid, False otherwise
        """
        # Check if reverse mapping is consistent
        for linq_field, acme_field in cls.LINQ_TO_ACME_MAPPING.items():
            if acme_field not in cls.ACME_TO_LINQ_MAPPING:
                return False
            if cls.ACME_TO_LINQ_MAPPING[acme_field] != linq_field:
                return False
        
        # Check if forward mapping is consistent
        for acme_field, linq_field in cls.ACME_TO_LINQ_MAPPING.items():
            if linq_field not in cls.LINQ_TO_ACME_MAPPING:
                return False
            if cls.LINQ_TO_ACME_MAPPING[linq_field] != acme_field:
                return False
        
        return True
