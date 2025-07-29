"""
Database schema inspection utilities.
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy import inspect, MetaData, Table
from sqlalchemy.engine import Engine
from ..core.exceptions import SchemaError

logger = logging.getLogger(__name__)


class SchemaInspector:
    """Utility for inspecting database schemas."""
    
    def __init__(self, engine: Engine):
        self.engine = engine
        self.inspector = inspect(engine)
        self.metadata = MetaData()
        
    def get_schema_summary(self) -> Dict[str, Any]:
        """Get a summary of the database schema for LLM context."""
        
        try:
            tables = {}
            table_names = self.inspector.get_table_names()
            
            for table_name in table_names:
                tables[table_name] = self._get_table_summary(table_name)
            
            return {
                'tables': tables,
                'table_count': len(tables),
                'dialect': self.engine.dialect.name
            }
            
        except Exception as e:
            logger.error(f"Failed to get schema summary: {e}")
            raise SchemaError(f"Schema inspection failed: {e}")
    
    def get_detailed_schema(self) -> Dict[str, Any]:
        """Get detailed schema information."""
        
        try:
            tables = {}
            table_names = self.inspector.get_table_names()
            
            for table_name in table_names:
                tables[table_name] = self._get_table_details(table_name)
            
            # Get views if supported
            views = {}
            try:
                view_names = self.inspector.get_view_names()
                for view_name in view_names:
                    views[view_name] = self._get_view_details(view_name)
            except Exception:
                pass  # Views not supported in all databases
            
            return {
                'tables': tables,
                'views': views,
                'table_count': len(tables),
                'view_count': len(views),
                'dialect': self.engine.dialect.name,
                'schema_names': self._get_schema_names()
            }
            
        except Exception as e:
            logger.error(f"Failed to get detailed schema: {e}")
            raise SchemaError(f"Detailed schema inspection failed: {e}")
    
    def _get_table_summary(self, table_name: str) -> Dict[str, Any]:
        """Get summary information for a single table."""
        
        try:
            columns = self.inspector.get_columns(table_name)
            primary_keys = self.inspector.get_pk_constraint(table_name)
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            
            # Simplify column information for LLM context
            simple_columns = []
            for col in columns:
                col_info = {
                    'name': col['name'],
                    'type': str(col['type']),
                    'nullable': col.get('nullable', True),
                    'primary_key': col['name'] in primary_keys.get('constrained_columns', [])
                }
                simple_columns.append(col_info)
            
            # Simplify foreign key information
            simple_fks = []
            for fk in foreign_keys:
                fk_info = f"{'.'.join(fk['constrained_columns'])} -> {fk['referred_table']}.{'.'.join(fk['referred_columns'])}"
                simple_fks.append(fk_info)
            
            return {
                'columns': simple_columns,
                'foreign_keys': simple_fks,
                'column_count': len(columns)
            }
            
        except Exception as e:
            logger.warning(f"Failed to get table summary for {table_name}: {e}")
            return {'error': str(e)}
    
    def _get_table_details(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information for a single table."""
        
        try:
            columns = self.inspector.get_columns(table_name)
            primary_keys = self.inspector.get_pk_constraint(table_name)
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            indexes = self.inspector.get_indexes(table_name)
            unique_constraints = self.inspector.get_unique_constraints(table_name)
            check_constraints = self.inspector.get_check_constraints(table_name)
            
            return {
                'columns': columns,
                'primary_key': primary_keys,
                'foreign_keys': foreign_keys,
                'indexes': indexes,
                'unique_constraints': unique_constraints,
                'check_constraints': check_constraints,
                'column_count': len(columns)
            }
            
        except Exception as e:
            logger.warning(f"Failed to get table details for {table_name}: {e}")
            return {'error': str(e)}
    
    def _get_view_details(self, view_name: str) -> Dict[str, Any]:
        """Get details for a database view."""
        
        try:
            columns = self.inspector.get_columns(view_name)
            
            return {
                'columns': columns,
                'column_count': len(columns),
                'type': 'view'
            }
            
        except Exception as e:
            logger.warning(f"Failed to get view details for {view_name}: {e}")
            return {'error': str(e)}
    
    def _get_schema_names(self) -> List[str]:
        """Get all schema names in the database."""
        
        try:
            return self.inspector.get_schema_names()
        except Exception:
            return []
    
    def get_table_names(self, schema: Optional[str] = None) -> List[str]:
        """Get table names, optionally filtered by schema."""
        
        try:
            return self.inspector.get_table_names(schema=schema)
        except Exception as e:
            logger.error(f"Failed to get table names: {e}")
            raise SchemaError(f"Failed to get table names: {e}")
    
    def get_column_names(self, table_name: str, schema: Optional[str] = None) -> List[str]:
        """Get column names for a specific table."""
        
        try:
            columns = self.inspector.get_columns(table_name, schema=schema)
            return [col['name'] for col in columns]
        except Exception as e:
            logger.error(f"Failed to get column names for {table_name}: {e}")
            raise SchemaError(f"Failed to get column names: {e}")
    
    def table_exists(self, table_name: str, schema: Optional[str] = None) -> bool:
        """Check if a table exists."""
        
        try:
            return self.inspector.has_table(table_name, schema=schema)
        except Exception as e:
            logger.error(f"Failed to check table existence for {table_name}: {e}")
            return False
    
    def get_relationships(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get relationships between tables."""
        
        relationships = {}
        
        try:
            table_names = self.inspector.get_table_names()
            
            for table_name in table_names:
                foreign_keys = self.inspector.get_foreign_keys(table_name)
                
                if foreign_keys:
                    relationships[table_name] = []
                    
                    for fk in foreign_keys:
                        rel_info = {
                            'type': 'foreign_key',
                            'from_table': table_name,
                            'from_columns': fk['constrained_columns'],
                            'to_table': fk['referred_table'],
                            'to_columns': fk['referred_columns']
                        }
                        relationships[table_name].append(rel_info)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Failed to get relationships: {e}")
            return {}
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample data from a table for context."""
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
                columns = result.keys()
                rows = result.fetchall()
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.warning(f"Failed to get sample data for {table_name}: {e}")
            return [] 