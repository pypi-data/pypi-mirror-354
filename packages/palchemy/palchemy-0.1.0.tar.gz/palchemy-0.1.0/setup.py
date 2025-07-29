from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="palchemy",
    version="0.1.0",
    author="Palchemy Contributors",
    author_email="contributors@palchemy.dev",
    description="A powerful Python library combining SQLAlchemy ORM with built-in LLM-powered text-to-SQL capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/palchemy/palchemy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.0.0",
        "sqlparse>=0.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "mysql": ["PyMySQL>=1.0.0"],
        "sqlite": ["aiosqlite>=0.19.0"],
        "postgresql": ["asyncpg>=0.28.0"],
    },
    entry_points={
        "console_scripts": [
            "palchemy=palchemy.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 