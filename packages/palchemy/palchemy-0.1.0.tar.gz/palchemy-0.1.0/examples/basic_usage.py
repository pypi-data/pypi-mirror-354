"""
Basic usage example for Palchemy.
"""

import os
from palchemy import Palchemy, Base, Column, Integer, String, DateTime
from datetime import datetime

# Define a simple model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

def main():
    # Initialize Palchemy with SQLite for demonstration
    db = Palchemy(
        database_url="sqlite:///example.db",
        llm_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo"
    )
    
    # Create tables
    Base.metadata.create_all(db.engine)
    
    # Add some sample data using traditional SQLAlchemy
    print("Adding sample data...")
    users = [
        User(name="Alice Johnson", email="alice@example.com"),
        User(name="Bob Smith", email="bob@example.com"),
        User(name="Charlie Brown", email="charlie@example.com"),
        User(name="Diana Wilson", email="diana@example.com"),
    ]
    
    session = db.session
    for user in users:
        session.add(user)
    session.commit()
    
    print("Sample data added successfully!")
    
    # Now use natural language queries
    print("\n=== Natural Language Queries ===")
    
    # Simple query
    print("\n1. Find all users:")
    result = db.query_natural("Show me all users")
    for user in result.data:
        print(f"  - {user['name']} ({user['email']})")
    
    print(f"Generated SQL: {result.sql}")
    
    # More complex query
    print("\n2. Find users with specific criteria:")
    result = db.query_natural("Find users whose names start with 'A' or 'B'")
    for user in result.data:
        print(f"  - {user['name']} ({user['email']})")
    
    print(f"Generated SQL: {result.sql}")
    
    # Query validation
    print("\n3. Query validation example:")
    query_info = db.validate_natural_query("Count how many users we have")
    print(f"Operation: {query_info.operation}")
    print(f"Tables involved: {', '.join(query_info.tables)}")
    print(f"Complexity: {query_info.complexity}")
    print(f"Generated SQL: {query_info.sql}")
    
    # Actually execute the count query
    result = db.query_natural("Count how many users we have")
    print(f"User count: {result.data[0] if result.data else 'No data'}")
    
    # Batch queries
    print("\n4. Batch queries:")
    queries = [
        "Count total users",
        "Find the first user by name alphabetically",
        "Show all email domains used"
    ]
    
    results = db.batch_query_natural(queries)
    for i, result in enumerate(results):
        if result:
            print(f"Query {i+1}: {queries[i]}")
            print(f"  Result: {result.data}")
            print(f"  SQL: {result.sql}")
        else:
            print(f"Query {i+1} failed")
    
    # Schema information
    print("\n5. Schema information:")
    schema = db.get_schema_info()
    print(f"Database has {schema['table_count']} tables:")
    for table_name, table_info in schema['tables'].items():
        print(f"  - {table_name}: {table_info['column_count']} columns")
    
    # Query history
    print("\n6. Query history:")
    history = db.get_query_history()
    print(f"Executed {len(history)} queries in this session")
    
    # Clean up
    db.close()
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main() 