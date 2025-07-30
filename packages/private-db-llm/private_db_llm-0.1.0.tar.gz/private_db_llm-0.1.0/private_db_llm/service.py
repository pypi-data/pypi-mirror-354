from typing import List, Dict, Any, Union
from mysql.connector import MySQLConnection
import psycopg2
from psycopg2.extensions import connection as PGConnection
import datetime
import re
from .config import LLMConfig
from .schema_extractor import SchemaExtractor as MySQLSchemaExtractor
from .schema_extractor_pg import PostgresSchemaExtractor
from .query_executor import QueryExecutor as MySQLQueryExecutor
from .query_executor_pg import PostgresQueryExecutor
from .llm_client import (
    LLMClient,
    OpenAIClient,
    OpenRouterClient,
    OllamaClient,
)

DEFAULT_INSTRUCTION = (
    f"Today is {datetime.datetime.now().date().isoformat()}."
    "You are a world-class data scientist and SQL expert. "
    "Based on the following database schema and user request, "
    "generate a one-run highly-optimized SQL query. "
    "Only output the SQL query without explanation.\n\n"
    "Schema:\n{schema}\n\n"
    "User request:\n{user_prompt}\n\n"
    "SQL:"
)

class DBLLMService:
    """Orchestrates schema extraction, LLM invocation, and query execution."""

    def __init__(
        self,
        llm_client: LLMClient,
        instruction_template: str = DEFAULT_INSTRUCTION
    ):
        self.llm = llm_client
        self.instruction = instruction_template

    def run(
        self,
        connection: Union[MySQLConnection, PGConnection],
        user_prompt: str
    ) -> List[Dict[str, Any]]:
        # 1. Choose schema extractor & executor by connection type
        if isinstance(connection, MySQLConnection):
            extractor = MySQLSchemaExtractor(connection)
            executor  = MySQLQueryExecutor(connection)
        elif isinstance(connection, PGConnection):
            extractor = PostgresSchemaExtractor(connection)
            executor  = PostgresQueryExecutor(connection)
        else:
            raise ValueError(f"Unsupported connection type: {type(connection)}")

        # 2. Extract schema
        schema = extractor.extract_schema()

        # 3. Build and send prompt
        print("Creating Schema...")
        schema_str = self._format_schema(schema)
        print("Sending Prompt...")
        prompt = self.instruction.format(
            schema=schema_str,
            user_prompt=user_prompt
        )
        raw_sql = self.llm.generate(prompt)
        sql = self._sanitize_sql(raw_sql)
        print(f"SQL: {sql}")

        # 4. Execute SQL and return JSON rows
        return executor.execute(sql)

    def _build_prompt(self, schema: Dict[str, Any], user_prompt: str) -> str:
        schema_str = self._format_schema(schema)
        return self.instruction.format(schema=schema_str, user_prompt=user_prompt)

    def _format_schema(self, schema: Dict[str, Any]) -> str:
        parts: List[str] = []
        for table, cols in schema["tables"].items():
            cols_fmt = ", ".join(f"{c['Field']} {c['Type']}" for c in cols)
            parts.append(f"{table}({cols_fmt})")
        relations = schema.get("relations")
        if relations:
            rels_fmt = "; ".join(
                f"{r['table']}.{r['column']}→"
                f"{r['ref_table']}.{r['ref_column']}"
                for r in relations
            )
            parts.append(f"Relations: {rels_fmt}")
        return "\n".join(parts)

    def _sanitize_sql(self, raw_sql: str) -> str:
        """
        Remove markdown code fences (```sql or ```) and any leading/trailing whitespace.
        """
        sql = raw_sql.strip()

        # Remove triple-backtick blocks
        # e.g., ```sql\nSELECT ...;\n```
        if sql.startswith("```"):
            # strip first fence
            sql = re.sub(r"^```(?:sql)?\s*", "", sql, count=1, flags=re.IGNORECASE)
        if sql.rstrip().endswith("```"):
            # strip trailing fence
            sql = re.sub(r"\s*```$", "", sql, count=1, flags=re.IGNORECASE)

        return sql.strip()

def create_service(config: LLMConfig) -> DBLLMService:
    """Factory: build a DBLLMService given an LLMConfig."""
    provider = config.provider.lower()
    if provider == "openai":
        client = OpenAIClient(config)
    elif provider == "openrouter":
        client = OpenRouterClient(config)
    elif provider == "ollama":
        client = OllamaClient(config)
    else:
        raise ValueError(f"Unsupported LLM provider: {config.provider}")
    return DBLLMService(client)
