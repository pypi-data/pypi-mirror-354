from typing import List, Dict, Any
from psycopg2.extensions import connection as PGConnection
from .exceptions import QueryExecutionError

class PostgresQueryExecutor:
    def __init__(self, conn: PGConnection):
        self.conn = conn

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            if cur.description:
                cols = [d[0] for d in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
            else:
                self.conn.commit()
                return []
        except Exception as e:
            raise QueryExecutionError(f"Postgres query failed: {e}") from e
        finally:
            cur.close()
