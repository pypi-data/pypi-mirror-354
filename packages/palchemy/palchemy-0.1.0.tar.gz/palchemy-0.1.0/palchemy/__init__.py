"""
Palchemy - A powerful Python library combining SQLAlchemy ORM with built-in LLM-powered text-to-SQL capabilities.
"""

__version__ = "0.1.0"
__author__ = "Palchemy Contributors"
__email__ = "contributors@palchemy.dev"

# Core imports
from .core.palchemy import Palchemy
from .core.config import LLMConfig, DatabaseConfig, PalchemyConfig
from .core.exceptions import (
    PalchemyError,
    LLMError,
    QueryValidationError,
    SchemaError,
    ConfigurationError
)

# SQLAlchemy re-exports for convenience
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Table,
    MetaData,
    create_engine,
    inspect
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Session
)
from sqlalchemy.sql import text

# Create the base for models
Base = declarative_base()

# LLM providers
from .llm.providers import OpenAIProvider, AnthropicProvider, CustomLLMProvider

# Utilities
from .utils.schema import SchemaInspector
from .utils.query_validator import QueryValidator
from .utils.security import QuerySanitizer

__all__ = [
    # Core classes
    "Palchemy",
    "LLMConfig",
    "DatabaseConfig",
    "PalchemyConfig",
    
    # Exceptions
    "PalchemyError",
    "LLMError",
    "QueryValidationError",
    "SchemaError",
    "ConfigurationError",
    
    # SQLAlchemy re-exports
    "Base",
    "Column",
    "Integer",
    "String",
    "Float",
    "Boolean",
    "DateTime",
    "Text",
    "ForeignKey",
    "Table",
    "MetaData",
    "create_engine",
    "inspect",
    "declarative_base",
    "sessionmaker",
    "relationship",
    "Session",
    "text",
    
    # LLM Providers
    "OpenAIProvider",
    "AnthropicProvider",
    "CustomLLMProvider",
    
    # Utilities
    "SchemaInspector",
    "QueryValidator",
    "QuerySanitizer",
] 