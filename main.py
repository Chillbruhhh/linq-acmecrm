"""Main FastAPI application for Linq-AcmeCRM integration."""

import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models.linq_models import LinqContact, LinqContactResponse
from models.acme_models import AcmeContactResponse
from services.auth_service import AuthService
from services.field_mapper import FieldMapper
from services.acme_service import AcmeService

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Linq-AcmeCRM Integration API",
    description="A lightweight CRM integration service that simulates how Linq would integrate with AcmeCRM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Security scheme
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get the current authenticated user.
    
    Args:
        credentials: JWT token from Authorization header
        
    Returns:
        Username of authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    return AuthService.get_current_user(token)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Linq-AcmeCRM Integration API",
        "version": "1.0.0",
        "docs": "/docs",
        "description": "FastAPI service for integrating Linq with AcmeCRM"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "linq-acmecrm-integration",
        "timestamp": "2025-07-25T16:38:00Z",
        "port": os.getenv("PORT", "8200")
    }


@app.post("/contacts", response_model=LinqContactResponse)
async def create_contact(
    contact: LinqContact,
    current_user: str = Depends(get_current_user)
) -> LinqContactResponse:
    """
    Create a new contact in AcmeCRM from Linq format.
    
    Args:
        contact: Contact data in Linq format
        current_user: Authenticated user
        
    Returns:
        LinqContactResponse with success status and AcmeCRM contact ID
        
    Raises:
        HTTPException: If contact creation fails
    """
    try:
        # Map from Linq format to AcmeCRM format
        acme_contact = FieldMapper.map_linq_to_acme(contact)
        
        # Create contact in AcmeCRM
        acme_response = AcmeService.create_contact(acme_contact)
        
        # Return success response
        return LinqContactResponse(
            success=True,
            contact_id=acme_response.acme_contact_id,
            message=f"Contact successfully created in AcmeCRM by user {current_user}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create contact: {str(e)}"
        )


@app.get("/contacts", response_model=List[LinqContact])
async def get_contacts(
    current_user: str = Depends(get_current_user)
) -> List[LinqContact]:
    """
    Retrieve all contacts from AcmeCRM in Linq format.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        List of contacts in Linq format
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        # Get all contacts from AcmeCRM
        acme_contacts = AcmeService.get_all_contacts()
        
        # Map contacts back to Linq format
        linq_contacts = []
        for acme_contact in acme_contacts:
            linq_contact = FieldMapper.map_acme_to_linq(acme_contact.acme_contact)
            linq_contacts.append(linq_contact)
        
        return linq_contacts
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve contacts: {str(e)}"
        )


@app.get("/contacts/stats")
async def get_contact_stats(current_user: str = Depends(get_current_user)):
    """
    Get statistics about contacts in AcmeCRM.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Dictionary with contact statistics
    """
    try:
        stats = AcmeService.get_storage_stats()
        return {
            "user": current_user,
            "acmecrm_stats": stats,
            "integration_status": "active"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve stats: {str(e)}"
        )


@app.get("/mapping/schema")
async def get_field_mapping_schema():
    """Get the field mapping schema between Linq and AcmeCRM formats."""
    return FieldMapper.get_mapping_schema()


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8200"))
    uvicorn.run(app, host=host, port=port)
