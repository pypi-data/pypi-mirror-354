"""
Advanced usage example for Palchemy showing custom providers and complex queries.
"""

import os
from palchemy import Palchemy, Base, Column, Integer, String, DateTime, ForeignKey, LLMConfig, DatabaseConfig, PalchemyConfig
from palchemy.llm.providers import CustomLLMProvider
from sqlalchemy.orm import relationship
from datetime import datetime

# Define models with relationships
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(Integer)  # Store as cents
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("Category", back_populates="products")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    customer_name = Column(String(100))
    order_date = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product")

def custom_llm_function(natural_query, system_prompt, config):
    """
    Example custom LLM function.
    In practice, this would call your custom LLM API.
    """
    # This is a mock implementation
    # You would replace this with actual LLM API calls
    
    query_lower = natural_query.lower()
    
    if "count" in query_lower and "product" in query_lower:
        return "SELECT COUNT(*) FROM products;"
    elif "expensive" in query_lower or "highest price" in query_lower:
        return "SELECT * FROM products ORDER BY price DESC LIMIT 5;"
    elif "categories" in query_lower:
        return "SELECT * FROM categories;"
    elif "orders" in query_lower and "total" in query_lower:
        return "SELECT SUM(quantity * p.price) as total FROM orders o JOIN products p ON o.product_id = p.id;"
    else:
        return "SELECT * FROM products LIMIT 10;"

def main():
    print("=== Advanced Palchemy Usage Example ===")
    
    # Configure Palchemy with custom settings
    database_config = DatabaseConfig(
        url="sqlite:///advanced_example.db",
        echo=False  # Set to True to see SQL queries
    )
    
    llm_config = LLMConfig(
        provider="openai",
        model="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.1,
        max_tokens=500
    )
    
    config = PalchemyConfig(
        database=database_config,
        llm=llm_config,
        enable_query_sanitization=True,
        enable_sql_injection_protection=True,
        max_query_length=5000,
        enable_audit_logging=True
    )
    
    # Initialize with custom configuration
    db = Palchemy(config=config)
    
    # Create tables
    Base.metadata.create_all(db.engine)
    
    # Add sample data
    print("Creating sample data...")
    
    # Categories
    categories = [
        Category(name="Electronics", description="Electronic devices and gadgets"),
        Category(name="Books", description="Books and publications"),
        Category(name="Clothing", description="Apparel and accessories"),
    ]
    
    session = db.session
    for category in categories:
        session.add(category)
    session.commit()
    
    # Products
    products = [
        Product(name="Smartphone", price=59999, category_id=1),  # $599.99
        Product(name="Laptop", price=129999, category_id=1),    # $1299.99
        Product(name="Python Programming Book", price=3999, category_id=2),  # $39.99
        Product(name="T-Shirt", price=1999, category_id=3),     # $19.99
        Product(name="Jeans", price=7999, category_id=3),       # $79.99
    ]
    
    for product in products:
        session.add(product)
    session.commit()
    
    # Orders
    orders = [
        Order(product_id=1, quantity=2, customer_name="John Doe"),
        Order(product_id=2, quantity=1, customer_name="Jane Smith"),
        Order(product_id=3, quantity=3, customer_name="Bob Johnson"),
        Order(product_id=1, quantity=1, customer_name="Alice Wilson"),
        Order(product_id=4, quantity=5, customer_name="Charlie Brown"),
    ]
    
    for order in orders:
        session.add(order)
    session.commit()
    
    print("Sample data created successfully!")
    
    # Complex natural language queries
    print("\n=== Complex Query Examples ===")
    
    queries = [
        "Show me all products with their categories",
        "Find the most expensive products in each category",
        "Calculate total revenue from all orders",
        "Show customers who bought electronics",
        "Find products that haven't been ordered yet",
        "Show average order value by product category",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        try:
            result = db.query_natural(query)
            print(f"   Execution time: {result.execution_time:.3f}s")
            print(f"   Generated SQL: {result.sql}")
            print(f"   Results: {len(result.data)} rows")
            
            # Show first few results
            for j, row in enumerate(result.data[:3]):
                print(f"     Row {j+1}: {row}")
            
            if len(result.data) > 3:
                print(f"     ... and {len(result.data) - 3} more rows")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    # Query enhancement example
    print("\n=== Query Enhancement Example ===")
    
    # Start with a basic SQLAlchemy query
    base_query = session.query(Product)
    print("Base query: SELECT products")
    
    # Enhance it with natural language
    try:
        enhanced_results = db.enhance_query_natural(
            base_query, 
            "only show products with price greater than $50 and sort by price descending"
        )
        print("Enhanced query executed successfully!")
        print(f"Results: {len(enhanced_results)} products")
        
    except Exception as e:
        print(f"Enhancement failed: {e}")
    
    # Custom LLM Provider example
    print("\n=== Custom LLM Provider Example ===")
    
    try:
        # Create a new instance with custom provider
        custom_config = PalchemyConfig(
            database=database_config,
            llm=LLMConfig(provider="custom")
        )
        
        custom_db = Palchemy(config=custom_config)
        
        # Set custom LLM provider (in practice, you'd do this differently)
        custom_db._llm_provider = CustomLLMProvider(
            custom_config.llm,
            generate_func=custom_llm_function
        )
        
        result = custom_db.query_natural("Show me the most expensive products")
        print("Custom LLM query successful!")
        print(f"Generated SQL: {result.sql}")
        print(f"Results: {len(result.data)} rows")
        
        custom_db.close()
        
    except Exception as e:
        print(f"Custom provider example failed: {e}")
    
    # Performance and security analysis
    print("\n=== Query Analysis ===")
    
    test_queries = [
        "SELECT * FROM products",
        "SELECT p.name, c.name FROM products p JOIN categories c ON p.category_id = c.id",
        "SELECT COUNT(*) FROM orders WHERE order_date > '2024-01-01'"
    ]
    
    for query in test_queries:
        try:
            analysis = db._query_validator.analyze_query(query)
            security_score = db._query_sanitizer.get_security_score(query)
            complexity_score = db._query_validator.get_query_complexity_score(query)
            
            print(f"Query: {query[:50]}...")
            print(f"  Operation: {analysis['operation']}")
            print(f"  Tables: {', '.join(analysis['tables'])}")
            print(f"  Complexity: {analysis['complexity']} (score: {complexity_score:.2f})")
            print(f"  Security risk: {security_score:.2f}")
            print()
            
        except Exception as e:
            print(f"Analysis failed for query: {e}")
    
    # Show query history and statistics
    print("=== Session Statistics ===")
    history = db.get_query_history()
    print(f"Total queries executed: {len(history)}")
    
    if history:
        total_time = sum(entry['execution_time'] for entry in history)
        avg_time = total_time / len(history)
        print(f"Total execution time: {total_time:.3f}s")
        print(f"Average execution time: {avg_time:.3f}s")
    
    # Clean up
    db.close()
    print("\nAdvanced example completed successfully!")

if __name__ == "__main__":
    main() 