"""
Concrete implementations of LLM providers.
"""

import logging
from typing import Optional, Dict, Any
import openai
import anthropic
from ..core.exceptions import LLMError, UnsupportedLLMProviderError, SQLGenerationError
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = openai.OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout
        )
    
    def generate_sql(self, natural_query: str, 
                    schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Generate SQL using OpenAI's API."""
        
        try:
            system_prompt = self._build_system_prompt(schema_info)
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Convert this to SQL: {natural_query}"}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            sql = response.choices[0].message.content
            return self._clean_sql_response(sql)
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMError(f"OpenAI API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI provider: {e}")
            raise SQLGenerationError(f"Failed to generate SQL: {e}")
    
    def enhance_sql(self, base_sql: str, enhancement: str,
                   schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Enhance SQL using OpenAI's API."""
        
        try:
            system_prompt = self._build_system_prompt(schema_info)
            system_prompt += "\n\nYour task is to enhance the provided SQL query based on the user's instructions."
            
            user_prompt = f"""
Base SQL Query:
{base_sql}

Enhancement Instructions:
{enhancement}

Please provide the enhanced SQL query.
"""
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            sql = response.choices[0].message.content
            return self._clean_sql_response(sql)
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMError(f"OpenAI API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI provider: {e}")
            raise SQLGenerationError(f"Failed to enhance SQL: {e}")


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM provider implementation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.client = anthropic.Anthropic(
            api_key=config.api_key,
            timeout=config.timeout
        )
    
    def generate_sql(self, natural_query: str, 
                    schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Generate SQL using Anthropic's API."""
        
        try:
            system_prompt = self._build_system_prompt(schema_info)
            
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Convert this to SQL: {natural_query}"}
                ]
            )
            
            sql = response.content[0].text
            return self._clean_sql_response(sql)
            
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise LLMError(f"Anthropic API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Anthropic provider: {e}")
            raise SQLGenerationError(f"Failed to generate SQL: {e}")
    
    def enhance_sql(self, base_sql: str, enhancement: str,
                   schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Enhance SQL using Anthropic's API."""
        
        try:
            system_prompt = self._build_system_prompt(schema_info)
            system_prompt += "\n\nYour task is to enhance the provided SQL query based on the user's instructions."
            
            user_prompt = f"""
Base SQL Query:
{base_sql}

Enhancement Instructions:
{enhancement}

Please provide the enhanced SQL query.
"""
            
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            sql = response.content[0].text
            return self._clean_sql_response(sql)
            
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise LLMError(f"Anthropic API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Anthropic provider: {e}")
            raise SQLGenerationError(f"Failed to enhance SQL: {e}")


class CustomLLMProvider(BaseLLMProvider):
    """Custom LLM provider for user-defined implementations."""
    
    def __init__(self, config, generate_func=None, enhance_func=None):
        super().__init__(config)
        self.generate_func = generate_func
        self.enhance_func = enhance_func
        
        if not generate_func:
            raise ValueError("generate_func is required for CustomLLMProvider")
    
    def generate_sql(self, natural_query: str, 
                    schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Generate SQL using custom function."""
        
        try:
            system_prompt = self._build_system_prompt(schema_info)
            sql = self.generate_func(
                natural_query=natural_query,
                system_prompt=system_prompt,
                config=self.config
            )
            return self._clean_sql_response(sql)
            
        except Exception as e:
            logger.error(f"Custom provider error: {e}")
            raise SQLGenerationError(f"Custom provider failed: {e}")
    
    def enhance_sql(self, base_sql: str, enhancement: str,
                   schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Enhance SQL using custom function."""
        
        if not self.enhance_func:
            raise NotImplementedError("enhance_func not provided to CustomLLMProvider")
        
        try:
            system_prompt = self._build_system_prompt(schema_info)
            sql = self.enhance_func(
                base_sql=base_sql,
                enhancement=enhancement,
                system_prompt=system_prompt,
                config=self.config
            )
            return self._clean_sql_response(sql)
            
        except Exception as e:
            logger.error(f"Custom provider error: {e}")
            raise SQLGenerationError(f"Custom provider failed: {e}")


def get_llm_provider(config) -> BaseLLMProvider:
    """Factory function to get the appropriate LLM provider."""
    
    provider_map = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "custom": CustomLLMProvider
    }
    
    if config.provider not in provider_map:
        raise UnsupportedLLMProviderError(f"Unsupported provider: {config.provider}")
    
    provider_class = provider_map[config.provider]
    
    try:
        return provider_class(config)
    except Exception as e:
        raise LLMError(f"Failed to initialize {config.provider} provider: {e}")