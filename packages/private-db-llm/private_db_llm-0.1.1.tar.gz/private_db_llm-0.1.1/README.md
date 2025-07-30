# private-db-llm

**Generate and execute SQL queries against MySQL or PostgreSQL using a Large Language Model (LLM)**

## Features

- **Schema Extraction**  
  Automatically discovers tables, columns, and foreign-key relations.
- **LLM-powered Query Generation**  
  Sends your prompt plus the database schema to an LLM and returns a syntactically valid SQL query.
- **Multi-Provider Support**  
  Works with OpenAI (v1+), OpenRouter, and Ollama HTTP APIs.
- **Multi-Database Support**  
  Out of the box, supports MySQL and PostgreSQL (via `mysql-connector-python` & `psycopg2-binary`).
- **SOLID Architecture**  
  Clean separation of concerns, easy to extend to other databases or LLM providers.

## Installation

```bash
pip install private-db-llm
```

### Optional extras:
- If you need PostgreSQL support, also install
```bash
pip install psycopg2-binary
```
- To load credentials from a .env file, you can add
```bash
pip install python-dotenv 
```

## Quick Start
### 1. Configure Your LLM
```python
from private_db_llm.config import LLMConfig

llm_conf = LLMConfig(
    provider="openai",      # "openai", "openrouter", or "ollama"
    api_key="sk-…",
    base_url=None,          # for OpenRouter or Ollama HTTP endpoint
    model="gpt-4o-mini"
)
```

### 2. Create the Service
```python
from private_db_llm.service import create_service

service = create_service(llm_conf)
```

### 3. Connect to Your Database
**MySQL**
```python
import mysql.connector

mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="your_mysql_password",
    database="your_mysql_db"
)
```
**PostgreSQL**
```python
import psycopg2

postgres_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres_user",
    password="your_pg_password",
    dbname="your_pg_db"
)
```

### 4. Run a Prompt & Get JSON Results
```python
# For MySQL
result_mysql = service.run(
    mysql_conn,
    "List all users who signed up in the last 7 days"
)
print(result_mysql)

# For PostgreSQL
result_pg = service.run(
    postgres_conn,
    "Show total sales per region for Q1"
)
print(result_pg)
```

## Advanced
- **Customizing the instruction template:**
  - Pass your own `instruction_template` to `DBLLMService` if you want to tweak how the LLM is prompted.

- **Adding a new database:**
  1. Create `<YourDB>SchemaExtractor` & `<YourDB>QueryExecutor` classes.
  2. Hook them into `service.run()` based on the connection type.

  - **Supporting another LLM provider:**
  1. Subclass the `LLMClient` ABC.
  2. Add your implementation in `llm_client.py`.
  3. Register it in `create_service()`.

## Version Compatibility
- Python: `>=3.12`
- OpenAI Python SDK: `>=1.0.0`
- MySQL driver: `mysql-connector-python>=8.0.0`
- HTTP client: `httpx>=0.23.0`
- PostgreSQL driver: `psycopg2-binary>=2.9.0`

## Contributing
1. Fork the repo
2. Create a feature branch
3. Write tests & update docs
4. Open a PR — all contributions welcome!

## License
MIT © Matin Khosravi