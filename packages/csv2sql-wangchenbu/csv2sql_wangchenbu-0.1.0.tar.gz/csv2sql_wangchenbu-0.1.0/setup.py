from setuptools import setup, find_packages

setup(
    name="csv2sql-wangchenbu",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "sqlalchemy",
        "click",
    ],
    extras_require={
        "mysql": ["mysqlclient"],
        "postgresql": ["psycopg2-binary"],
        "sqlite": [],
        "oracle": ["cx_Oracle"],
        "mssql": ["pyodbc"],
    },
    entry_points={
        "console_scripts": [
            "csv2sql=csv2sql.cli:main",
        ],
    },
    author="wangchenbu",
    author_email="3206590839@qq.com",
    description="Convert CSV files to SQL create table and insert statements",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wangchenbu/csv2sql",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="csv, sql, database, conversion, etl",
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/csv2sql/issues",
        "Source": "https://github.com/yourusername/csv2sql",
        "Documentation": "https://github.com/yourusername/csv2sql#readme",
    },
) 