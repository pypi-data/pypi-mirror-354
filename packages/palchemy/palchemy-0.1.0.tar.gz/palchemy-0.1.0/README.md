# Palchemy 🧪

**A powerful Python library combining SQLAlchemy ORM with built-in LLM-powered text-to-SQL capabilities**

Palchemy bridges the gap between traditional database operations and modern AI-powered natural language queries. Write SQL using natural language, while maintaining all the power and flexibility of SQLAlchemy.

## Features

- 🔗 **Full SQLAlchemy Integration**: All the power of SQLAlchemy ORM
- 🤖 **Built-in Text-to-SQL**: Convert natural language to SQL using LLMs
- 🔌 **Multiple LLM Support**: OpenAI GPT, Anthropic Claude, and more
- 🗄️ **Multi-Database Support**: PostgreSQL, MySQL, SQLite
- ⚡ **Easy Configuration**: Simple setup with API keys
- 🛡️ **Type Safety**: Full typing support with Pydantic

## Installation

```bash
pip install palchemy
```

For development:
```bash
pip install palchemy[dev]
```

For specific database support:
```bash
pip install palchemy[postgresql]  # For PostgreSQL with asyncpg
pip install palchemy[mysql]       # For MySQL support
pip install palchemy[sqlite]      # For SQLite with aiosqlite
```

## Quick Start

### 1. Basic Setup

```python
from palchemy import Palchemy
import os

# Initialize with your database and LLM settings
db = Palchemy(
    database_url="postgresql://user:password@localhost/dbname",
    llm_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4"
)
```

### 2. Traditional SQLAlchemy Usage

```python
from palchemy import Palchemy, Base, Column, Integer, String
from sqlalchemy.orm import declarative_base

# Define your models (standard SQLAlchemy)
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

# Traditional database operations
user = User(name="John Doe", email="john@example.com")
db.session.add(user)
db.session.commit()
```

### 3. Natural Language Queries

```python
# Query using natural language
users = db.query_natural("Find all users who registered last month")

# Complex queries
results = db.query_natural(
    "Show me the top 5 customers by total order value, "
    "including their email and registration date"
)

# Get the generated SQL (for debugging/learning)
sql_query = db.last_generated_sql
print(f"Generated SQL: {sql_query}")
```

### 4. Hybrid Approach

```python
# Combine natural language with traditional methods
base_query = db.session.query(User)
enhanced_results = db.enhance_query_natural(
    base_query,
    "filter by users who made purchases in the last 30 days"
)
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
PALCHEMY_DEFAULT_MODEL=gpt-4
PALCHEMY_DEFAULT_PROVIDER=openai
```

### Programmatic Configuration

```python
from palchemy import Palchemy, LLMConfig

# Advanced LLM configuration
llm_config = LLMConfig(
    provider="openai",
    model="gpt-4",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)

db = Palchemy(
    database_url="your_database_url",
    llm_config=llm_config
)
```

## Advanced Features

### Schema-Aware Queries

Palchemy automatically provides your database schema to the LLM for more accurate SQL generation:

```python
# The LLM knows your table structure
results = db.query_natural(
    "Find users with the highest order totals",
    include_schema=True  # Default: True
)
```

### Query Validation

```python
# Validate queries before execution
query_info = db.validate_natural_query(
    "Show me all users and their orders"
)

print(f"Estimated cost: {query_info.estimated_cost}")
print(f"Query complexity: {query_info.complexity}")
print(f"Tables involved: {query_info.tables}")
```

### Batch Operations

```python
# Process multiple natural language queries
queries = [
    "Count total users",
    "Find average order value",
    "List top 10 products by sales"
]

results = db.batch_query_natural(queries)
```

## Supported LLM Providers

- **OpenAI**: GPT-3.5, GPT-4, GPT-4 Turbo
- **Anthropic**: Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus
- **Custom**: Extend with your own LLM provider

## Security Features

- **SQL Injection Protection**: All generated queries are validated
- **Query Sanitization**: Automatic cleaning of potentially harmful queries
- **Access Control**: Role-based query restrictions
- **Audit Logging**: Track all natural language queries and generated SQL

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://palchemy.readthedocs.io)
- 💬 [Discord Community](https://discord.gg/palchemy)
- 🐛 [Issue Tracker](https://github.com/palchemy/palchemy/issues)
- 📧 [Email Support](mailto:support@palchemy.dev)

---

**Made with ❤️ by the Palchemy team** 