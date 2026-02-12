from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRole:
    STUDENT = "student"
    READER = "reader"


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True
    role: str = UserRole.READER  # student or reader


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: str
    email: EmailStr
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    """
    Schema for updating a user
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserLogin(BaseModel):
    """
    Schema for user login
    """
    email: EmailStr
    password: str


class User(UserBase):
    """
    Represents a platform user with authentication credentials, profile information, and learning history
    """
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True  # Enable ORM mode


class LoginResponse(BaseModel):
    """
    Schema for login response
    """
    access_token: str
    token_type: str
    user: User