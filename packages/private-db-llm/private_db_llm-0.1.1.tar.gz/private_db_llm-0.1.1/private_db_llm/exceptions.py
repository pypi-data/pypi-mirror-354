class SchemaExtractionError(Exception):
    """Raised when extracting DB schema fails."""

class LLMResponseError(Exception):
    """Raised when LLM does not return a valid SQL query."""

class QueryExecutionError(Exception):
    """Raised when executing the generated SQL on the database fails."""
