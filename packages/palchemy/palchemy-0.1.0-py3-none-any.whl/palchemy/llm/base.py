"""
Base classes for LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseLLMProvider(ABC):
    """Base class for all LLM providers."""
    
    def __init__(self, config):
        self.config = config
    
    @abstractmethod
    def generate_sql(self, natural_query: str, 
                    schema_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate SQL from natural language query.
        
        Args:
            natural_query: Natural language description of the query
            schema_info: Database schema information
            
        Returns:
            Generated SQL query string
        """
        pass
    
    @abstractmethod
    def enhance_sql(self, base_sql: str, enhancement: str,
                   schema_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Enhance an existing SQL query with natural language instructions.
        
        Args:
            base_sql: Existing SQL query
            enhancement: Natural language enhancement instructions
            schema_info: Database schema information
            
        Returns:
            Enhanced SQL query string
        """
        pass
    
    def _build_system_prompt(self, schema_info: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt for SQL generation."""
        
        base_prompt = """You are a SQL expert. Your task is to convert natural language queries into valid SQL statements.

Guidelines:
1. Generate only valid SQL queries
2. Use proper SQL syntax and formatting
3. Consider database schema when provided
4. Avoid SQL injection patterns
5. Use appropriate JOINs when needed
6. Return only the SQL query, no explanations

"""
        
        if schema_info:
            schema_text = self._format_schema_info(schema_info)
            base_prompt += f"\nDatabase Schema:\n{schema_text}\n"
        
        return base_prompt
    
    def _format_schema_info(self, schema_info: Dict[str, Any]) -> str:
        """Format schema information for the prompt."""
        
        if not schema_info:
            return ""
        
        formatted = []
        
        for table_name, table_info in schema_info.get('tables', {}).items():
            formatted.append(f"Table: {table_name}")
            
            if 'columns' in table_info:
                for col in table_info['columns']:
                    col_def = f"  - {col['name']} ({col['type']}"
                    if col.get('primary_key'):
                        col_def += ", PRIMARY KEY"
                    if col.get('nullable') is False:
                        col_def += ", NOT NULL"
                    col_def += ")"
                    formatted.append(col_def)
            
            if 'foreign_keys' in table_info:
                for fk in table_info['foreign_keys']:
                    formatted.append(f"  - FOREIGN KEY: {fk}")
            
            formatted.append("")  # Empty line between tables
        
        return "\n".join(formatted)
    
    def _clean_sql_response(self, response: str) -> str:
        """Clean and extract SQL from LLM response."""
        
        # Remove common prefixes/suffixes
        response = response.strip()
        
        # Remove markdown code blocks
        if response.startswith('```sql'):
            response = response[6:]
        elif response.startswith('```'):
            response = response[3:]
        
        if response.endswith('```'):
            response = response[:-3]
        
        # Remove common explanatory text
        lines = response.split('\n')
        sql_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip explanatory lines
            if line.lower().startswith(('this query', 'the above', 'explanation:', 'note:')):
                continue
            
            sql_lines.append(line)
        
        sql = '\n'.join(sql_lines).strip()
        
        # Ensure it ends with semicolon
        if sql and not sql.endswith(';'):
            sql += ';'
        
        return sql 