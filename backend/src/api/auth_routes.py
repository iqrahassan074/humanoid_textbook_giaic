from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from typing import Optional
import os
import logging
from passlib.context import CryptContext
from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import EmailStr

# Import models
from ..models.user import User, UserCreate, UserLogin, LoginResponse
from ..db import get_db, User as DBUser
from ..auth import create_access_token, get_current_user, get_current_active_user
from ..exceptions import ValidationError, AuthenticationError, DatabaseError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # Truncate password to 72 characters to comply with bcrypt limitations
    truncated_password = password[:72]
    return pwd_context.hash(truncated_password)

@router.post("/register", response_model=LoginResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account
    """
    logger.info(f"Registering new user: {user_data.email}")

    try:
        # Validate input data
        if len(user_data.password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        
        if len(user_data.password) > 72:
            raise ValidationError("Password must be no more than 72 characters long")
        
        # Check if user already exists
        existing_user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash password
        password_hash = get_password_hash(user_data.password)

        # Create new user
        db_user = DBUser(
            email=user_data.email,
            password_hash=password_hash,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role='reader'  # Default role
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email, "user_id": str(db_user.id)},
            expires_delta=access_token_expires
        )

        logger.info(f"Successfully registered user: {user_data.email}")

        # Convert DB user to Pydantic user
        user_response = User(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at or db_user.created_at,
            is_active=db_user.is_active,
            role=db_user.role
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}", exc_info=True)
        raise DatabaseError(detail="Failed to register user due to database error")


@router.post("/login", response_model=LoginResponse)
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    logger.info(f"Login attempt for: {credentials.email}")

    try:
        # Get user from database
        user = db.query(DBUser).filter(DBUser.email == credentials.email).first()
        
        if not user or not user.is_active:
            raise AuthenticationError("Invalid credentials")
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=access_token_expires
        )

        logger.info(f"Successfully logged in user: {credentials.email}")

        # Convert DB user to Pydantic user
        user_response = User(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            updated_at=user.updated_at or user.created_at,
            is_active=user.is_active,
            role=user.role
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        raise DatabaseError(detail="Failed to authenticate user due to database error")


@router.post("/logout")
async def logout_user():
    """
    Invalidate user session (in a real app, this might involve token blacklisting)
    """
    logger.info("User logout requested")
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve information about the authenticated user
    """
    logger.info("Retrieving current user info")
    return current_user