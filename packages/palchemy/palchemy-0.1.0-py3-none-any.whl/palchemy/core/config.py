"""
Configuration classes for Palchemy.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    CUSTOM = "custom"


class DatabaseDialect(str, Enum):
    """Supported database dialects."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    
    provider: LLMProvider = Field(default=LLMProvider.OPENAI)
    model: str = Field(default="gpt-3.5-turbo")
    api_key: Optional[str] = Field(default=None)
    base_url: Optional[str] = Field(default=None)
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0)
    timeout: int = Field(default=30, gt=0)
    retry_attempts: int = Field(default=3, ge=0)
    custom_headers: Optional[Dict[str, str]] = Field(default=None)
    
    @validator('api_key', always=True)
    def validate_api_key(cls, v, values):
        if v is None:
            provider = values.get('provider', LLMProvider.OPENAI)
            if provider == LLMProvider.OPENAI:
                v = os.getenv('OPENAI_API_KEY')
            elif provider == LLMProvider.ANTHROPIC:
                v = os.getenv('ANTHROPIC_API_KEY')
            
            if v is None and provider != LLMProvider.CUSTOM:
                raise ValueError(f"API key is required for {provider} provider")
        
        return v
    
    @validator('model')
    def validate_model(cls, v, values):
        provider = values.get('provider', LLMProvider.OPENAI)
        
        valid_models = {
            LLMProvider.OPENAI: [
                "gpt-3.5-turbo", "gpt-3.5-turbo-16k",
                "gpt-4", "gpt-4-turbo", "gpt-4-turbo-preview"
            ],
            LLMProvider.ANTHROPIC: [
                "claude-3-haiku-20240307", "claude-3-sonnet-20240229",
                "claude-3-opus-20240229"
            ]
        }
        
        if provider in valid_models and v not in valid_models[provider]:
            raise ValueError(f"Invalid model {v} for provider {provider}")
        
        return v


class DatabaseConfig(BaseModel):
    """Configuration for database connections."""
    
    url: str
    dialect: Optional[DatabaseDialect] = Field(default=None)
    pool_size: int = Field(default=5, gt=0)
    max_overflow: int = Field(default=10, ge=0)
    pool_timeout: int = Field(default=30, gt=0)
    pool_recycle: int = Field(default=3600, gt=0)
    echo: bool = Field(default=False)
    connect_args: Optional[Dict[str, Any]] = Field(default=None)
    
    @validator('dialect', always=True)
    def infer_dialect(cls, v, values):
        if v is None:
            url = values.get('url', '')
            if url.startswith('postgresql'):
                return DatabaseDialect.POSTGRESQL
            elif url.startswith('mysql'):
                return DatabaseDialect.MYSQL
            elif url.startswith('sqlite'):
                return DatabaseDialect.SQLITE
        return v


class PalchemyConfig(BaseModel):
    """Main configuration for Palchemy."""
    
    database: DatabaseConfig
    llm: LLMConfig
    
    # Security settings
    enable_query_sanitization: bool = Field(default=True)
    enable_sql_injection_protection: bool = Field(default=True)
    max_query_length: int = Field(default=10000, gt=0)
    allowed_operations: List[str] = Field(
        default=["SELECT", "INSERT", "UPDATE", "DELETE"]
    )
    blocked_keywords: List[str] = Field(
        default=["DROP", "TRUNCATE", "ALTER", "CREATE"]
    )
    
    # Performance settings
    enable_query_caching: bool = Field(default=True)
    cache_ttl: int = Field(default=300, gt=0)  # 5 minutes
    enable_schema_caching: bool = Field(default=True)
    schema_cache_ttl: int = Field(default=3600, gt=0)  # 1 hour
    
    # Logging settings
    enable_audit_logging: bool = Field(default=True)
    log_level: str = Field(default="INFO")
    log_queries: bool = Field(default=True)
    log_llm_requests: bool = Field(default=False)
    
    class Config:
        use_enum_values = True


def load_config_from_env() -> PalchemyConfig:
    """Load configuration from environment variables."""
    
    database_config = DatabaseConfig(
        url=os.getenv('DATABASE_URL', 'sqlite:///palchemy.db')
    )
    
    llm_config = LLMConfig(
        provider=os.getenv('PALCHEMY_LLM_PROVIDER', 'openai'),
        model=os.getenv('PALCHEMY_LLM_MODEL', 'gpt-3.5-turbo'),
        api_key=os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
    )
    
    return PalchemyConfig(
        database=database_config,
        llm=llm_config
    ) 