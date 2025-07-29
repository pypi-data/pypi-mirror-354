"""
Custom exceptions for Palchemy library.
"""

class PalchemyError(Exception):
    """Base exception for all Palchemy-related errors."""
    pass


class LLMError(PalchemyError):
    """Raised when there's an error with LLM operations."""
    pass


class QueryValidationError(PalchemyError):
    """Raised when a query fails validation."""
    pass


class SchemaError(PalchemyError):
    """Raised when there's an error with database schema operations."""
    pass


class ConfigurationError(PalchemyError):
    """Raised when there's a configuration error."""
    pass


class DatabaseConnectionError(PalchemyError):
    """Raised when there's a database connection error."""
    pass


class SQLGenerationError(LLMError):
    """Raised when SQL generation fails."""
    pass


class UnsupportedLLMProviderError(LLMError):
    """Raised when an unsupported LLM provider is specified."""
    pass


class SecurityError(PalchemyError):
    """Raised when a security violation is detected."""
    pass 