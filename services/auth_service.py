"""Mock JWT authentication service for Linq-AcmeCRM integration."""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from pydantic import BaseModel


class TokenData(BaseModel):
    """Model for JWT token data."""
    
    username: Optional[str] = None


class AuthService:
    """Service for handling mock JWT authentication."""
    
    SECRET_KEY = "linq-assessment-secret-key-2024"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Mock valid tokens for testing
    MOCK_VALID_TOKENS = {
        "linq-demo-token": "demo_user",
        "linq-assessment-token": "assessment_user",
        "linq-sales-engineer": "sales_user"
    }
    
    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a mock JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Optional expiration time delta
            
        Returns:
            JWT token string
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def verify_token(cls, token: str) -> TokenData:
        """
        Verify a JWT token and return token data.
        
        Args:
            token: JWT token to verify
            
        Returns:
            TokenData with username
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        # Check mock tokens first for demo purposes
        if token in cls.MOCK_VALID_TOKENS:
            return TokenData(username=cls.MOCK_VALID_TOKENS[token])
        
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return TokenData(username=username)
        except JWTError:
            raise credentials_exception
    
    @classmethod
    def get_current_user(cls, token: str) -> str:
        """
        Get the current authenticated user from token.
        
        Args:
            token: JWT token from Authorization header
            
        Returns:
            Username of authenticated user
            
        Raises:
            HTTPException: If authentication fails
        """
        token_data = cls.verify_token(token)
        if token_data.username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data.username
