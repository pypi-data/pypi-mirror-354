from typing import List, Dict, Any
from mysql.connector import MySQLConnection
from .exceptions import QueryExecutionError

class QueryExecutor:
    """Executes the generated SQL and returns rows as JSON."""

    def __init__(self, connection: MySQLConnection):
        self.conn = connection

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(sql)
            # if it's a SELECT
            if cursor.with_rows:
                return cursor.fetchall()
            else:
                self.conn.commit()
                return []
        except Exception as e:
            raise QueryExecutionError(f"Failed to execute SQL: {e}") from e
        finally:
            cursor.close()
