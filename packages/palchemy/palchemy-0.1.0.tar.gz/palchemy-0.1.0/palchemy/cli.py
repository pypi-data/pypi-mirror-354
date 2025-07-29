"""
Command-line interface for Palchemy.
"""

import argparse
import sys
import os
from .core.palchemy import Palchemy
from .core.config import load_config_from_env
from .core.exceptions import PalchemyError


def main():
    """Main CLI entry point."""
    
    parser = argparse.ArgumentParser(
        description="Palchemy - SQLAlchemy with built-in LLM text-to-SQL capabilities"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="palchemy 0.1.0"
    )
    
    parser.add_argument(
        "--query", 
        "-q",
        help="Natural language query to execute"
    )
    
    parser.add_argument(
        "--database-url",
        "-d",
        help="Database connection URL"
    )
    
    parser.add_argument(
        "--provider",
        "-p",
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM provider to use"
    )
    
    parser.add_argument(
        "--model",
        "-m",
        help="LLM model to use"
    )
    
    parser.add_argument(
        "--api-key",
        "-k",
        help="API key for LLM provider"
    )
    
    parser.add_argument(
        "--schema",
        action="store_true",
        help="Show database schema information"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate query without executing"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize Palchemy
        if args.database_url:
            db = Palchemy(
                database_url=args.database_url,
                llm_provider=args.provider,
                api_key=args.api_key,
                model=args.model
            )
        else:
            config = load_config_from_env()
            db = Palchemy(config=config)
        
        if args.schema:
            # Show schema information
            schema_info = db.get_schema_info()
            print("Database Schema:")
            print(f"Dialect: {schema_info.get('dialect', 'Unknown')}")
            print(f"Tables: {schema_info.get('table_count', 0)}")
            
            for table_name, table_info in schema_info.get('tables', {}).items():
                print(f"\nTable: {table_name}")
                print(f"  Columns: {table_info.get('column_count', 0)}")
                
                for col in table_info.get('columns', [])[:5]:  # Show first 5 columns
                    print(f"    - {col['name']} ({col['type']})")
        
        elif args.query:
            if args.validate:
                # Validate query without executing
                query_info = db.validate_natural_query(args.query)
                print("Query Validation Results:")
                print(f"Operation: {query_info.operation}")
                print(f"Tables: {', '.join(query_info.tables)}")
                print(f"Complexity: {query_info.complexity}")
                print(f"Generated SQL: {query_info.sql}")
            else:
                # Execute query
                result = db.query_natural(args.query)
                
                print(f"Query executed successfully!")
                print(f"Execution time: {result.execution_time:.3f}s")
                print(f"Rows returned: {result.row_count}")
                print(f"Generated SQL: {result.sql}")
                
                if result.data:
                    print("\nResults:")
                    # Show first few rows
                    for i, row in enumerate(result.data[:10]):  # Show first 10 rows
                        print(f"Row {i+1}: {row}")
                    
                    if len(result.data) > 10:
                        print(f"... and {len(result.data) - 10} more rows")
        else:
            parser.print_help()
    
    except PalchemyError as e:
        print(f"Palchemy error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 