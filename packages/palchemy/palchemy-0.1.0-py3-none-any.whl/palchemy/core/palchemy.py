"""
Main Palchemy class combining SQLAlchemy with LLM-powered text-to-SQL.
"""

import logging
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
from sqlalchemy.engine import Engine

from .config import PalchemyConfig, LLMConfig, DatabaseConfig, load_config_from_env
from .exceptions import (
    PalchemyError, DatabaseConnectionError, LLMError, 
    QueryValidationError, ConfigurationError
)
from ..llm.providers import get_llm_provider
from ..utils.schema import SchemaInspector
from ..utils.query_validator import QueryValidator
from ..utils.security import QuerySanitizer

logger = logging.getLogger(__name__)


class QueryResult:
    """Container for query results with metadata."""
    
    def __init__(self, data: List[Dict[str, Any]], sql: str, 
                 execution_time: float, row_count: int):
        self.data = data
        self.sql = sql
        self.execution_time = execution_time
        self.row_count = row_count
        self.timestamp = datetime.now()
    
    def __repr__(self):
        return f"QueryResult(rows={self.row_count}, time={self.execution_time:.3f}s)"
    
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]


class QueryInfo:
    """Information about a validated query."""
    
    def __init__(self, sql: str, tables: List[str], operation: str,
                 complexity: str, estimated_cost: str):
        self.sql = sql
        self.tables = tables
        self.operation = operation
        self.complexity = complexity
        self.estimated_cost = estimated_cost


class Palchemy:
    """
    Main Palchemy class combining SQLAlchemy ORM with LLM-powered text-to-SQL.
    """
    
    def __init__(self, 
                 database_url: Optional[str] = None,
                 llm_provider: Optional[str] = None,
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 config: Optional[PalchemyConfig] = None,
                 **kwargs):
        """
        Initialize Palchemy instance.
        
        Args:
            database_url: Database connection URL
            llm_provider: LLM provider ('openai', 'anthropic', 'custom')
            api_key: API key for LLM provider
            model: Model name to use
            config: Complete PalchemyConfig object
            **kwargs: Additional configuration options
        """
        
        # Load configuration
        if config:
            self.config = config
        else:
            self.config = self._build_config(
                database_url, llm_provider, api_key, model, **kwargs
            )
        
        # Initialize components
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._session: Optional[Session] = None
        self._llm_provider = None
        self._schema_inspector: Optional[SchemaInspector] = None
        self._query_validator: Optional[QueryValidator] = None
        self._query_sanitizer: Optional[QuerySanitizer] = None
        
        # Query history
        self._last_generated_sql: Optional[str] = None
        self._query_history: List[Dict[str, Any]] = []
        
        # Initialize database connection
        self._setup_database()
        
        # Initialize LLM provider
        self._setup_llm()
        
        # Initialize utilities
        self._setup_utilities()
        
        logger.info("Palchemy initialized successfully")
    
    def _build_config(self, database_url: Optional[str], llm_provider: Optional[str],
                      api_key: Optional[str], model: Optional[str], **kwargs) -> PalchemyConfig:
        """Build configuration from parameters."""
        
        if not database_url:
            try:
                return load_config_from_env()
            except Exception as e:
                raise ConfigurationError(f"No database URL provided and failed to load from env: {e}")
        
        db_config = DatabaseConfig(url=database_url, **kwargs)
        llm_config = LLMConfig(
            provider=llm_provider or "openai",
            model=model or "gpt-3.5-turbo",
            api_key=api_key
        )
        
        return PalchemyConfig(database=db_config, llm=llm_config)
    
    def _setup_database(self):
        """Initialize database connection and session."""
        try:
            self._engine = create_engine(
                self.config.database.url,
                pool_size=self.config.database.pool_size,
                max_overflow=self.config.database.max_overflow,
                pool_timeout=self.config.database.pool_timeout,
                pool_recycle=self.config.database.pool_recycle,
                echo=self.config.database.echo,
                **(self.config.database.connect_args or {})
            )
            
            self._session_factory = sessionmaker(
                bind=self._engine,
                expire_on_commit=False
            )
            
            # Test connection
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info(f"Database connection established: {self.config.database.dialect}")
            
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to connect to database: {e}")
    
    def _setup_llm(self):
        """Initialize LLM provider."""
        try:
            self._llm_provider = get_llm_provider(self.config.llm)
            logger.info(f"LLM provider initialized: {self.config.llm.provider}")
        except Exception as e:
            raise LLMError(f"Failed to initialize LLM provider: {e}")
    
    def _setup_utilities(self):
        """Initialize utility classes."""
        self._schema_inspector = SchemaInspector(self._engine)
        self._query_validator = QueryValidator(self.config)
        self._query_sanitizer = QuerySanitizer(self.config)
    
    @property
    def session(self) -> Session:
        """Get current database session."""
        if self._session is None:
            self._session = self._session_factory()
        return self._session
    
    @property
    def engine(self) -> Engine:
        """Get database engine."""
        return self._engine
    
    @property
    def last_generated_sql(self) -> Optional[str]:
        """Get the last generated SQL query."""
        return self._last_generated_sql
    
    def query_natural(self, natural_query: str, 
                     include_schema: bool = True,
                     validate: bool = True) -> QueryResult:
        """
        Execute a natural language query.
        
        Args:
            natural_query: Natural language description of the query
            include_schema: Whether to include schema information for LLM
            validate: Whether to validate the generated SQL
        
        Returns:
            QueryResult object with data and metadata
        """
        
        start_time = datetime.now()
        
        try:
            # Get database schema if requested
            schema_info = None
            if include_schema:
                schema_info = self._schema_inspector.get_schema_summary()
            
            # Generate SQL using LLM
            sql_query = self._llm_provider.generate_sql(
                natural_query=natural_query,
                schema_info=schema_info
            )
            
            self._last_generated_sql = sql_query
            
            # Validate and sanitize if enabled
            if validate:
                if self.config.enable_query_sanitization:
                    sql_query = self._query_sanitizer.sanitize(sql_query)
                
                if not self._query_validator.validate_sql(sql_query):
                    raise QueryValidationError("Generated SQL failed validation")
            
            # Execute query
            result = self._execute_sql(sql_query)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Log query
            self._log_query(natural_query, sql_query, execution_time)
            
            return QueryResult(
                data=result,
                sql=sql_query,
                execution_time=execution_time,
                row_count=len(result)
            )
            
        except Exception as e:
            logger.error(f"Natural query failed: {e}")
            raise PalchemyError(f"Failed to execute natural query: {e}")
    
    def validate_natural_query(self, natural_query: str) -> QueryInfo:
        """
        Validate a natural language query without executing it.
        
        Args:
            natural_query: Natural language description of the query
        
        Returns:
            QueryInfo object with validation details
        """
        
        try:
            schema_info = self._schema_inspector.get_schema_summary()
            sql_query = self._llm_provider.generate_sql(
                natural_query=natural_query,
                schema_info=schema_info
            )
            
            validation_result = self._query_validator.analyze_query(sql_query)
            
            return QueryInfo(
                sql=sql_query,
                tables=validation_result.get('tables', []),
                operation=validation_result.get('operation', 'UNKNOWN'),
                complexity=validation_result.get('complexity', 'UNKNOWN'),
                estimated_cost=validation_result.get('estimated_cost', 'UNKNOWN')
            )
            
        except Exception as e:
            raise QueryValidationError(f"Failed to validate query: {e}")
    
    def batch_query_natural(self, queries: List[str]) -> List[QueryResult]:
        """
        Execute multiple natural language queries in batch.
        
        Args:
            queries: List of natural language queries
        
        Returns:
            List of QueryResult objects
        """
        
        results = []
        for query in queries:
            try:
                result = self.query_natural(query)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch query failed for '{query}': {e}")
                # Continue with other queries
                results.append(None)
        
        return results
    
    def enhance_query_natural(self, base_query, natural_enhancement: str):
        """
        Enhance an existing SQLAlchemy query with natural language.
        
        Args:
            base_query: Existing SQLAlchemy query object
            natural_enhancement: Natural language description of enhancement
        
        Returns:
            Enhanced query results
        """
        
        try:
            # Convert base query to SQL
            base_sql = str(base_query.statement.compile(
                dialect=self._engine.dialect, 
                compile_kwargs={"literal_binds": True}
            ))
            
            # Get schema info
            schema_info = self._schema_inspector.get_schema_summary()
            
            # Generate enhanced SQL
            enhanced_sql = self._llm_provider.enhance_sql(
                base_sql=base_sql,
                enhancement=natural_enhancement,
                schema_info=schema_info
            )
            
            self._last_generated_sql = enhanced_sql
            
            # Execute enhanced query
            result = self._execute_sql(enhanced_sql)
            
            return result
            
        except Exception as e:
            raise PalchemyError(f"Failed to enhance query: {e}")
    
    def _execute_sql(self, sql: str) -> List[Dict[str, Any]]:
        """Execute raw SQL and return results."""
        
        with self._engine.connect() as conn:
            result = conn.execute(text(sql))
            
            if result.returns_rows:
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
            else:
                return []
    
    def _log_query(self, natural_query: str, sql: str, execution_time: float):
        """Log query execution."""
        
        if self.config.enable_audit_logging:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'natural_query': natural_query,
                'generated_sql': sql,
                'execution_time': execution_time,
                'user': 'system'  # Could be enhanced with actual user info
            }
            
            self._query_history.append(log_entry)
            
            if self.config.log_queries:
                logger.info(f"Query executed: {natural_query[:100]}... -> {execution_time:.3f}s")
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get detailed database schema information."""
        return self._schema_inspector.get_detailed_schema()
    
    def get_query_history(self) -> List[Dict[str, Any]]:
        """Get query execution history."""
        return self._query_history.copy()
    
    def close(self):
        """Close database connections and cleanup."""
        if self._session:
            self._session.close()
        if self._engine:
            self._engine.dispose()
        logger.info("Palchemy connections closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 