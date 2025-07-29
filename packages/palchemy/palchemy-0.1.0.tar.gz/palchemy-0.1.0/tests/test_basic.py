"""
Basic tests for Palchemy library.
"""

import pytest
import os
from palchemy import Palchemy, Base, Column, Integer, String
from palchemy.core.config import LLMConfig, DatabaseConfig, PalchemyConfig
from palchemy.core.exceptions import PalchemyError, ConfigurationError


class TestUser(Base):
    __tablename__ = 'test_users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(200))


def test_palchemy_initialization():
    """Test basic Palchemy initialization."""
    
    # Test with SQLite (no API key required for initialization)
    db = Palchemy(
        database_url="sqlite:///:memory:",
        llm_provider="openai",
        api_key="test_key",
        model="gpt-3.5-turbo"
    )
    
    assert db is not None
    assert db.config.database.url == "sqlite:///:memory:"
    assert db.config.llm.provider == "openai"
    
    db.close()


def test_configuration_validation():
    """Test configuration validation."""
    
    # Test invalid LLM provider
    with pytest.raises(ValueError):
        LLMConfig(
            provider="invalid_provider",
            api_key="test_key"
        )
    
    # Test valid configuration
    config = LLMConfig(
        provider="openai",
        model="gpt-3.5-turbo",
        api_key="test_key"
    )
    
    assert config.provider == "openai"
    assert config.model == "gpt-3.5-turbo"


def test_database_operations():
    """Test basic database operations."""
    
    db = Palchemy(
        database_url="sqlite:///:memory:",
        llm_provider="openai",
        api_key="test_key"
    )
    
    # Create table
    Base.metadata.create_all(db.engine)
    
    # Add test data
    user = TestUser(name="Test User", email="test@example.com")
    db.session.add(user)
    db.session.commit()
    
    # Query using SQLAlchemy
    users = db.session.query(TestUser).all()
    assert len(users) == 1
    assert users[0].name == "Test User"
    
    db.close()


def test_schema_inspection():
    """Test schema inspection functionality."""
    
    db = Palchemy(
        database_url="sqlite:///:memory:",
        llm_provider="openai",
        api_key="test_key"
    )
    
    # Create table
    Base.metadata.create_all(db.engine)
    
    # Test schema inspection
    schema_info = db.get_schema_info()
    
    assert 'tables' in schema_info
    assert 'test_users' in schema_info['tables']
    assert schema_info['table_count'] >= 1
    
    table_info = schema_info['tables']['test_users']
    assert 'columns' in table_info
    assert table_info['column_count'] >= 3  # id, name, email
    
    db.close()


def test_query_validation():
    """Test SQL query validation."""
    
    db = Palchemy(
        database_url="sqlite:///:memory:",
        llm_provider="openai",
        api_key="test_key"
    )
    
    # Test valid query
    valid_sql = "SELECT * FROM test_users;"
    assert db._query_validator.validate_sql(valid_sql) == True
    
    # Test query analysis
    analysis = db._query_validator.analyze_query(valid_sql)
    assert analysis['operation'] == 'SELECT'
    assert 'test_users' in analysis['tables']
    
    db.close()


def test_security_features():
    """Test security and sanitization features."""
    
    db = Palchemy(
        database_url="sqlite:///:memory:",
        llm_provider="openai",
        api_key="test_key"
    )
    
    # Test SQL sanitization
    dangerous_sql = "SELECT * FROM users; DROP TABLE users; --"
    sanitized = db._query_sanitizer.sanitize(dangerous_sql)
    
    # Should remove the dangerous parts
    assert "DROP" not in sanitized.upper()
    
    # Test security scoring
    safe_sql = "SELECT * FROM users"
    dangerous_sql_2 = "SELECT * FROM users; DROP TABLE users"
    
    safe_score = db._query_sanitizer.get_security_score(safe_sql)
    dangerous_score = db._query_sanitizer.get_security_score(dangerous_sql_2)
    
    assert safe_score < dangerous_score
    
    db.close()


def test_error_handling():
    """Test error handling."""
    
    # Test invalid database URL
    with pytest.raises(Exception):  # Should raise some form of database error
        db = Palchemy(
            database_url="invalid://url",
            llm_provider="openai",
            api_key="test_key"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 