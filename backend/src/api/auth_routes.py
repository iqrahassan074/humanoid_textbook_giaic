from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from typing import Optional
import os
import jwt
import logging
from passlib.context import CryptContext

# Import models - using dict as placeholder since we don't have full DB implementation
from ..models.content_chunk import ContentChunk

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# In a real implementation, users would be stored in a database
# For now, using placeholder data to demonstrate the API structure
USERS_DB = {
    "user@example.com": {
        "id": "1",
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password_hash": "$2b$12$JvCwu667F.C6FzkdQ4n67OgXN2.bpTQqH.8z8Zz4YyVZ4zZ8Z4YyV",  # Placeholder hash
        "is_active": True,
        "role": "student",  # or "reader"
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # For demo purposes, we'll use a dummy check
    # In real implementation: return pwd_context.verify(plain_password, hashed_password)
    return True  # Placeholder for demonstration

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # In real implementation: return pwd_context.hash(password)
    return "$2b$12$JvCwu667F.C6FzkdQ4n67OgXN2.bpTQqH.8z8Zz4YyVZ4zZ8Z4YyV"  # Placeholder

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode a JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(lambda: None)):  # Placeholder for real dependency
    """Get current user from token"""
    pass

@router.post("/register", response_model=dict)
async def register_user(user_data: dict):
    """
    Create a new user account
    """
    logger.info(f"Registering new user: {user_data.get('email')}")

    email = user_data.get("email")
    password = user_data.get("password")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")

    # Validate input
    if not email or not password or not first_name or not last_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, password, first name, and last name are required"
        )

    # Check if user already exists
    if email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash password (placeholder)
    password_hash = get_password_hash(password)

    # Create user ID
    user_id = str(len(USERS_DB) + 1)

    # Create new user
    new_user = {
        "id": user_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password_hash": password_hash,
        "is_active": True,
        "role": "reader",  # Default role
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    USERS_DB[email] = new_user

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email, "user_id": user_id},
        expires_delta=access_token_expires
    )

    logger.info(f"Successfully registered user: {email}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user["id"],
            "email": new_user["email"],
            "first_name": new_user["first_name"],
            "last_name": new_user["last_name"],
            "role": new_user["role"],
            "created_at": new_user["created_at"],
            "updated_at": new_user["updated_at"]
        }
    }


@router.post("/login", response_model=dict)
async def login_user(credentials: dict):
    """
    Authenticate user and return JWT token
    """
    logger.info(f"Login attempt for: {credentials.get('email')}")

    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    # Get user from database
    user = USERS_DB.get(email)
    if not user or not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password (placeholder)
    # if not verify_password(password, user["password_hash"]):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials"
    #     )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]},
        expires_delta=access_token_expires
    )

    logger.info(f"Successfully logged in user: {email}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "role": user["role"],
            "created_at": user["created_at"],
            "updated_at": user["updated_at"]
        }
    }


@router.post("/logout")
async def logout_user():
    """
    Invalidate user session (in a real app, this might involve token blacklisting)
    """
    logger.info("User logout requested")
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=dict)
async def get_current_user(token: str = None):  # In a real app, this would use Depends(oauth2_scheme)
    """
    Retrieve information about the authenticated user
    """
    logger.info("Retrieving current user info")

    # In a real implementation, this would decode the JWT token
    # For this demo, returning a sample user
    if not token:
        # Simulate a valid token by returning a sample user
        sample_user = {
            "id": "1",
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "student",
            "created_at": "2025-12-15T00:00:00Z",
            "updated_at": "2025-12-15T00:00:00Z",
            "is_active": True
        }
        return sample_user

    try:
        # Decode the token to get user info
        payload = decode_access_token(token.split(" ")[1] if " " in token else token)
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        user = USERS_DB.get(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


# Utility function for dependency injection
async def get_current_active_user(token: str = None):
    """
    Get the current active user (used as dependency)
    """
    user = await get_current_user(token)
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user