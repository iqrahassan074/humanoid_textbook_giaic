from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
import logging

logger = logging.getLogger(__name__)

class CustomException(HTTPException):
    """Custom exception class for the application"""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class ValidationError(CustomException):
    """Exception raised for validation errors"""
    def __init__(self, detail: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(status_code=422, detail=detail, error_code=error_code)


class AuthenticationError(CustomException):
    """Exception raised for authentication errors"""
    def __init__(self, detail: str = "Authentication failed", error_code: str = "AUTH_ERROR"):
        super().__init__(status_code=401, detail=detail, error_code=error_code)


class AuthorizationError(CustomException):
    """Exception raised for authorization errors"""
    def __init__(self, detail: str = "Not authorized", error_code: str = "AUTHORIZATION_ERROR"):
        super().__init__(status_code=403, detail=detail, error_code=error_code)


class ResourceNotFoundError(CustomException):
    """Exception raised when a resource is not found"""
    def __init__(self, resource_type: str, resource_id: str = None, error_code: str = "RESOURCE_NOT_FOUND"):
        if resource_id:
            detail = f"{resource_type} with ID '{resource_id}' not found"
        else:
            detail = f"{resource_type} not found"
        super().__init__(status_code=404, detail=detail, error_code=error_code)


class DatabaseError(CustomException):
    """Exception raised for database errors"""
    def __init__(self, detail: str = "Database error occurred", error_code: str = "DATABASE_ERROR"):
        super().__init__(status_code=500, detail=detail, error_code=error_code)


class BusinessLogicError(CustomException):
    """Exception raised for business logic errors"""
    def __init__(self, detail: str, error_code: str = "BUSINESS_LOGIC_ERROR"):
        super().__init__(status_code=400, detail=detail, error_code=error_code)


# Exception handlers
async def custom_exception_handler(request: Request, exc: CustomException):
    """Handle custom exceptions"""
    logger.error(f"Custom exception: {exc.detail} (Code: {getattr(exc, 'error_code', 'UNKNOWN')})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.detail,
                "code": getattr(exc, 'error_code', 'UNKNOWN')
            }
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP exception: {exc.detail} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "status_code": exc.status_code
            }
        }
    )


async def validation_error_handler(request: Request, exc: Union[ValidationError, HTTPException]):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.detail}")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "ValidationError",
                "message": exc.detail,
                "status_code": 422
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"General exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred",
                "status_code": 500
            }
        }
    )