"""
Security utilities for SQL query sanitization and protection.
"""

import re
import logging
from typing import List, Dict, Any
import sqlparse
from ..core.exceptions import SecurityError

logger = logging.getLogger(__name__)


class QuerySanitizer:
    """Utility for sanitizing SQL queries to prevent security issues."""
    
    def __init__(self, config):
        self.config = config
        self.blocked_keywords = [kw.upper() for kw in config.blocked_keywords]
    
    def sanitize(self, sql: str) -> str:
        """
        Sanitize a SQL query by removing or escaping potentially dangerous content.
        
        Args:
            sql: SQL query string to sanitize
            
        Returns:
            Sanitized SQL query string
            
        Raises:
            SecurityError: If query contains unremovable security risks
        """
        
        try:
            # Remove comments
            sql = self._remove_comments(sql)
            
            # Remove excessive whitespace
            sql = self._normalize_whitespace(sql)
            
            # Check for and remove dangerous patterns
            sql = self._remove_dangerous_patterns(sql)
            
            # Validate final result
            if self._has_critical_security_issues(sql):
                raise SecurityError("Query contains critical security issues that cannot be sanitized")
            
            return sql
            
        except Exception as e:
            logger.error(f"Query sanitization failed: {e}")
            raise SecurityError(f"Failed to sanitize query: {e}")
    
    def _remove_comments(self, sql: str) -> str:
        """Remove SQL comments from the query."""
        
        # Remove single-line comments (-- style)
        sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        
        # Remove multi-line comments (/* */ style)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        
        return sql
    
    def _normalize_whitespace(self, sql: str) -> str:
        """Normalize whitespace in the SQL query."""
        
        # Replace multiple whitespace characters with single space
        sql = re.sub(r'\s+', ' ', sql)
        
        # Strip leading/trailing whitespace
        sql = sql.strip()
        
        return sql
    
    def _remove_dangerous_patterns(self, sql: str) -> str:
        """Remove or neutralize dangerous SQL patterns."""
        
        # List of dangerous patterns to remove/neutralize
        dangerous_patterns = [
            # Command execution
            (r'\bxp_cmdshell\b', ''),
            (r'\bsp_executesql\b', ''),
            
            # File operations
            (r'\bbulk\s+insert\b', ''),
            (r'\bopenrowset\b', ''),
            (r'\bopendatasource\b', ''),
            
            # System procedures
            (r'\bsp_addlogin\b', ''),
            (r'\bsp_addsrvrolemember\b', ''),
            (r'\bsp_configure\b', ''),
            
            # Multiple statement separators (excessive semicolons)
            (r';\s*;+', ';'),
        ]
        
        for pattern, replacement in dangerous_patterns:
            sql = re.sub(pattern, replacement, sql, flags=re.IGNORECASE)
        
        return sql
    
    def _has_critical_security_issues(self, sql: str) -> bool:
        """Check if the query still contains critical security issues."""
        
        critical_patterns = [
            # Stacked queries with dangerous operations
            r';\s*(DROP|TRUNCATE|ALTER|CREATE)\s+',
            
            # Union-based injection attempts
            r'UNION\s+ALL\s+SELECT.*--',
            
            # Time-based blind injection
            r'WAITFOR\s+DELAY',
            r'SLEEP\s*\(',
            
            # Error-based injection
            r'AND\s+\d+=\d+--',
            r'OR\s+\d+=\d+--',
            
            # System function calls
            r'@@VERSION',
            r'USER_NAME\(\)',
            r'DB_NAME\(\)',
        ]
        
        sql_upper = sql.upper()
        
        for pattern in critical_patterns:
            if re.search(pattern, sql_upper, re.IGNORECASE):
                return True
        
        return False
    
    def escape_string_literals(self, sql: str) -> str:
        """Escape string literals in SQL to prevent injection."""
        
        # This is a basic implementation
        # In production, consider using parameterized queries instead
        
        # Escape single quotes by doubling them
        def escape_quotes(match):
            content = match.group(1).replace("'", "''")
            return f"'{content}'"
        
        sql = re.sub(r"'([^']*)'", escape_quotes, sql)
        
        return sql
    
    def validate_identifiers(self, sql: str) -> bool:
        """Validate that all identifiers (table names, column names) are safe."""
        
        # Extract potential identifiers
        identifiers = self._extract_identifiers(sql)
        
        for identifier in identifiers:
            if not self._is_safe_identifier(identifier):
                logger.warning(f"Unsafe identifier detected: {identifier}")
                return False
        
        return True
    
    def _extract_identifiers(self, sql: str) -> List[str]:
        """Extract identifiers from SQL query."""
        
        # This is a simplified implementation
        # For production, use a proper SQL parser
        
        # Pattern to match potential identifiers
        identifier_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        
        # Extract all potential identifiers
        identifiers = re.findall(identifier_pattern, sql)
        
        # Filter out SQL keywords
        sql_keywords = {
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE',
            'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'ON', 'AS',
            'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET',
            'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN', 'LIKE',
            'IS', 'NULL', 'TRUE', 'FALSE', 'DISTINCT', 'ALL', 'ANY',
            'UNION', 'INTERSECT', 'EXCEPT', 'CASE', 'WHEN', 'THEN',
            'ELSE', 'END', 'CAST', 'CONVERT', 'COUNT', 'SUM', 'AVG',
            'MIN', 'MAX', 'SUBSTRING', 'UPPER', 'LOWER', 'TRIM'
        }
        
        return [identifier for identifier in identifiers if identifier.upper() not in sql_keywords]
    
    def _is_safe_identifier(self, identifier: str) -> bool:
        """Check if an identifier is safe."""
        
        # Basic safety checks
        if not identifier:
            return False
        
        # Must start with letter or underscore
        if not re.match(r'^[a-zA-Z_]', identifier):
            return False
        
        # Must contain only alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', identifier):
            return False
        
        # Must not be too long
        if len(identifier) > 64:  # Common database limit
            return False
        
        # Must not match blocked patterns
        blocked_patterns = [
            r'^(sp_|xp_|fn_)',  # System procedures/functions
            r'(admin|root|sa|sys)',  # Admin-related names
        ]
        
        for pattern in blocked_patterns:
            if re.search(pattern, identifier, re.IGNORECASE):
                return False
        
        return True
    
    def get_security_score(self, sql: str) -> float:
        """
        Calculate a security risk score for the query (0.0 to 1.0).
        
        Args:
            sql: SQL query string
            
        Returns:
            Security risk score between 0.0 (safe) and 1.0 (very risky)
        """
        
        risk_score = 0.0
        
        # Check for various risk factors
        risk_factors = [
            (r';\s*DROP\b', 0.9),  # Drop operations
            (r';\s*DELETE\b', 0.7),  # Uncontrolled delete
            (r'UNION\s+SELECT', 0.6),  # Union injection
            (r'--', 0.3),  # Comments (potential obfuscation)
            (r'/\*.*\*/', 0.3),  # Multi-line comments
            (r"'\s*OR\s+'", 0.8),  # OR injection pattern
            (r'EXEC\s*\(', 0.9),  # Dynamic execution
            (r'xp_cmdshell', 1.0),  # System command execution
            (r'sp_executesql', 0.7),  # Dynamic SQL execution
            (r'WAITFOR\s+DELAY', 0.8),  # Time-based attacks
        ]
        
        sql_upper = sql.upper()
        
        for pattern, weight in risk_factors:
            if re.search(pattern, sql_upper, re.IGNORECASE):
                risk_score += weight
        
        # Normalize to 0-1 range
        return min(1.0, risk_score)
    
    def get_sanitization_report(self, original_sql: str, sanitized_sql: str) -> Dict[str, Any]:
        """Generate a report comparing original and sanitized SQL."""
        
        return {
            'original_length': len(original_sql),
            'sanitized_length': len(sanitized_sql),
            'changes_made': original_sql != sanitized_sql,
            'original_security_score': self.get_security_score(original_sql),
            'sanitized_security_score': self.get_security_score(sanitized_sql),
            'risk_reduction': self.get_security_score(original_sql) - self.get_security_score(sanitized_sql)
        } 