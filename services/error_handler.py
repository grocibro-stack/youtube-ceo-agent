"""Error handling utilities."""
from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import AppException, AIServiceError, ValidationError, ConfigurationError
from utils.logger import get_logger
from typing import Callable

logger = get_logger(__name__)


def handle_service_error(error: Exception) -> dict:
    """
    Convert exceptions to API response format.
    
    Args:
        error: Exception to handle
    
    Returns:
        Dictionary with success and error fields
    """
    logger.error(f"Handling error: {type(error).__name__}: {str(error)}")
    
    if isinstance(error, AppException):
        return {
            "success": False,
            "error": error.message,
            "error_code": error.error_code
        }
    
    # Generic error handling
    return {
        "success": False,
        "error": str(error),
        "error_code": "UNKNOWN_ERROR"
    }


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for FastAPI.
    
    Args:
        request: The request that caused the error
        exc: The exception
    
    Returns:
        JSON response with error details
    """
    logger.error(f"Global exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": exc.message,
                "error_code": exc.error_code
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )
