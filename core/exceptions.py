"""Custom exceptions for the application."""


class AppException(Exception):
    """Base exception for the application."""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class AIServiceError(AppException):
    """Raised when AI service (OpenRouter) fails."""
    
    def __init__(self, message: str = "AI service error", error_code: str = "AI_SERVICE_ERROR"):
        super().__init__(message, error_code)


class ValidationError(AppException):
    """Raised when validation fails."""
    
    def __init__(self, message: str = "Validation error", error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, error_code)


class ConfigurationError(AppException):
    """Raised when configuration is missing or invalid."""
    
    def __init__(self, message: str = "Configuration error", error_code: str = "CONFIG_ERROR"):
        super().__init__(message, error_code)
