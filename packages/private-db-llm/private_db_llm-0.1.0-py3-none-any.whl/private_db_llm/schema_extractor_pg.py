from typing import Dict, Any
import psycopg2
from psycopg2.extensions import connection as PGConnection
from .exceptions import SchemaExtractionError

class PostgresSchemaExtractor:
    def __init__(self, conn: PGConnection):
        self.conn = conn

    def extract_schema(self) -> Dict[str, Any]:
        try:
            cur = self.conn.cursor()
            # 1. get all tables in public schema
            cur.execute("""
                SELECT table_name
                  FROM information_schema.tables
                 WHERE table_schema = 'public'
            """)
            tables = [r[0] for r in cur.fetchall()]

            schema = {"tables": {}, "relations": []}

            # 2. columns
            for tbl in tables:
                cur.execute(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                      FROM information_schema.columns
                     WHERE table_name = %s
                """, (tbl,))
                cols = [
                    {
                        "Field": c[0],
                        "Type": c[1],
                        "Null": c[2],
                        "Default": c[3],
                    }
                    for c in cur.fetchall()
                ]
                schema["tables"][tbl] = cols

            # 3. FKs
            cur.execute("""
                SELECT
                  kcu.table_name, kcu.column_name,
                  ccu.table_name AS foreign_table,
                  ccu.column_name AS foreign_column
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                  ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = 'public';
            """)
            schema["relations"] = [
                {
                    "table": r[0],
                    "column": r[1],
                    "ref_table": r[2],
                    "ref_column": r[3],
                }
                for r in cur.fetchall()
            ]

            return schema

        except Exception as e:
            raise SchemaExtractionError(f"Postgres schema extraction failed: {e}") from e
        finally:
            cur.close()
