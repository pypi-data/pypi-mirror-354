from typing import Dict, Any
from mysql.connector import MySQLConnection
from .exceptions import SchemaExtractionError

class SchemaExtractor:
    """Extracts tables, columns, and foreign-key relations from MySQL."""

    def __init__(self, connection: MySQLConnection):
        self.conn = connection

    def extract_schema(self) -> Dict[str, Any]:
        try:
            cursor = self.conn.cursor()
            # get all tables
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]

            schema = {"tables": {}, "relations": []}

            # describe each table
            for tbl in tables:
                cursor.execute(f"DESCRIBE `{tbl}`")
                cols = [
                    {
                        "Field": c[0],
                        "Type": c[1],
                        "Null": c[2],
                        "Key": c[3],
                        "Default": c[4],
                        "Extra": c[5],
                    }
                    for c in cursor.fetchall()
                ]
                schema["tables"][tbl] = cols

            # foreign keys via information_schema
            cursor.execute(
                """
                SELECT TABLE_NAME, COLUMN_NAME,
                       REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND REFERENCED_TABLE_NAME IS NOT NULL
                """
            )
            schema["relations"] = [
                {
                    "table": r[0],
                    "column": r[1],
                    "ref_table": r[2],
                    "ref_column": r[3],
                }
                for r in cursor.fetchall()
            ]

            return schema

        except Exception as e:
            raise SchemaExtractionError(f"Failed to extract schema: {e}") from e

        finally:
            cursor.close()
