"""Core module with exceptions and base classes."""
from .exceptions import (
    AIServiceError,
    ValidationError,
    ConfigurationError,
)

__all__ = [
    "AIServiceError",
    "ValidationError", 
    "ConfigurationError",
]
