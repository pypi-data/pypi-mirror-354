"""
SQL query validation and analysis utilities.
"""

import re
import logging
from typing import Dict, List, Any, Optional
import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import Keyword, DML, DDL
from ..core.exceptions import QueryValidationError

logger = logging.getLogger(__name__)


class QueryValidator:
    """Utility for validating and analyzing SQL queries."""
    
    def __init__(self, config):
        self.config = config
        self.blocked_keywords = [kw.upper() for kw in config.blocked_keywords]
        self.allowed_operations = [op.upper() for op in config.allowed_operations]
    
    def validate_sql(self, sql: str) -> bool:
        """
        Validate a SQL query against security and configuration rules.
        
        Args:
            sql: SQL query string to validate
            
        Returns:
            True if query is valid, False otherwise
        """
        
        try:
            # Basic length check
            if len(sql) > self.config.max_query_length:
                logger.warning(f"Query too long: {len(sql)} > {self.config.max_query_length}")
                return False
            
            # Parse the SQL
            parsed = sqlparse.parse(sql)
            if not parsed:
                logger.warning("Failed to parse SQL query")
                return False
            
            # Check each statement
            for statement in parsed:
                if not self._validate_statement(statement):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Query validation error: {e}")
            return False
    
    def analyze_query(self, sql: str) -> Dict[str, Any]:
        """
        Analyze a SQL query and return metadata.
        
        Args:
            sql: SQL query string to analyze
            
        Returns:
            Dictionary with query analysis results
        """
        
        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                raise QueryValidationError("Failed to parse SQL query")
            
            analysis = {
                'tables': [],
                'operation': 'UNKNOWN',
                'complexity': 'LOW',
                'estimated_cost': 'LOW',
                'has_joins': False,
                'has_subqueries': False,
                'has_aggregations': False,
                'statement_count': len(parsed)
            }
            
            for statement in parsed:
                stmt_analysis = self._analyze_statement(statement)
                
                # Merge results
                analysis['tables'].extend(stmt_analysis.get('tables', []))
                
                if stmt_analysis.get('operation') != 'UNKNOWN':
                    analysis['operation'] = stmt_analysis['operation']
                
                if stmt_analysis.get('has_joins'):
                    analysis['has_joins'] = True
                    analysis['complexity'] = 'MEDIUM'
                
                if stmt_analysis.get('has_subqueries'):
                    analysis['has_subqueries'] = True
                    analysis['complexity'] = 'HIGH'
                
                if stmt_analysis.get('has_aggregations'):
                    analysis['has_aggregations'] = True
            
            # Remove duplicates from tables
            analysis['tables'] = list(set(analysis['tables']))
            
            # Estimate cost based on complexity
            if analysis['complexity'] == 'HIGH':
                analysis['estimated_cost'] = 'HIGH'
            elif analysis['complexity'] == 'MEDIUM':
                analysis['estimated_cost'] = 'MEDIUM'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Query analysis error: {e}")
            raise QueryValidationError(f"Failed to analyze query: {e}")
    
    def _validate_statement(self, statement: Statement) -> bool:
        """Validate a single SQL statement."""
        
        # Get the first meaningful token to determine operation type
        operation = self._get_statement_operation(statement)
        
        if operation and operation not in self.allowed_operations:
            logger.warning(f"Operation {operation} not allowed")
            return False
        
        # Check for blocked keywords
        sql_text = str(statement).upper()
        for blocked_keyword in self.blocked_keywords:
            if blocked_keyword in sql_text:
                logger.warning(f"Blocked keyword found: {blocked_keyword}")
                return False
        
        # Check for potential SQL injection patterns
        if self.config.enable_sql_injection_protection:
            if self._has_injection_patterns(sql_text):
                logger.warning("Potential SQL injection detected")
                return False
        
        return True
    
    def _analyze_statement(self, statement: Statement) -> Dict[str, Any]:
        """Analyze a single SQL statement."""
        
        analysis = {
            'operation': self._get_statement_operation(statement),
            'tables': self._extract_table_names(statement),
            'has_joins': self._has_joins(statement),
            'has_subqueries': self._has_subqueries(statement),
            'has_aggregations': self._has_aggregations(statement)
        }
        
        return analysis
    
    def _get_statement_operation(self, statement: Statement) -> Optional[str]:
        """Extract the main operation from a SQL statement."""
        
        for token in statement.flatten():
            if token.ttype in (DML, DDL):
                return token.value.upper()
            elif token.ttype is Keyword and token.value.upper() in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']:
                return token.value.upper()
        
        return None
    
    def _extract_table_names(self, statement: Statement) -> List[str]:
        """Extract table names from a SQL statement."""
        
        tables = []
        sql_text = str(statement).upper()
        
        # Simple regex patterns for table extraction
        # Note: This is a basic implementation. For production, consider using a proper SQL parser
        patterns = [
            r'\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\bJOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\bINTO\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\bUPDATE\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, sql_text)
            tables.extend(matches)
        
        return list(set(tables))  # Remove duplicates
    
    def _has_joins(self, statement: Statement) -> bool:
        """Check if statement contains JOIN operations."""
        sql_text = str(statement).upper()
        join_keywords = ['JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN']
        return any(keyword in sql_text for keyword in join_keywords)
    
    def _has_subqueries(self, statement: Statement) -> bool:
        """Check if statement contains subqueries."""
        sql_text = str(statement)
        # Count parentheses to detect subqueries (basic heuristic)
        open_parens = sql_text.count('(')
        close_parens = sql_text.count(')')
        return open_parens > 0 and close_parens > 0 and open_parens == close_parens
    
    def _has_aggregations(self, statement: Statement) -> bool:
        """Check if statement contains aggregation functions."""
        sql_text = str(statement).upper()
        agg_functions = ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'GROUP BY', 'HAVING']
        return any(func in sql_text for func in agg_functions)
    
    def _has_injection_patterns(self, sql_text: str) -> bool:
        """Check for common SQL injection patterns."""
        
        injection_patterns = [
            r";\s*(DROP|DELETE|INSERT|UPDATE)",
            r"UNION\s+SELECT",
            r"--\s*\w",  # SQL comments
            r"/\*.*\*/",  # Multi-line comments
            r"'\s*OR\s+'.*'=.*'",  # Classic OR injection
            r"'\s*;\s*--",  # Statement termination
            r"EXEC\s*\(",  # Command execution
            r"xp_cmdshell",  # System command execution
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, sql_text, re.IGNORECASE):
                return True
        
        return False
    
    def get_query_complexity_score(self, sql: str) -> float:
        """
        Calculate a complexity score for the query (0.0 to 1.0).
        
        Args:
            sql: SQL query string
            
        Returns:
            Complexity score between 0.0 (simple) and 1.0 (very complex)
        """
        
        try:
            analysis = self.analyze_query(sql)
            score = 0.0
            
            # Base complexity
            if analysis['operation'] in ['SELECT']:
                score += 0.1
            elif analysis['operation'] in ['INSERT', 'UPDATE', 'DELETE']:
                score += 0.2
            
            # Table count
            table_count = len(analysis['tables'])
            if table_count > 1:
                score += min(0.3, table_count * 0.1)
            
            # Features
            if analysis['has_joins']:
                score += 0.2
            if analysis['has_subqueries']:
                score += 0.3
            if analysis['has_aggregations']:
                score += 0.1
            
            # Multiple statements
            if analysis['statement_count'] > 1:
                score += 0.2
            
            return min(1.0, score)
            
        except Exception as e:
            logger.error(f"Complexity calculation error: {e}")
            return 0.5  # Default to medium complexity on error 