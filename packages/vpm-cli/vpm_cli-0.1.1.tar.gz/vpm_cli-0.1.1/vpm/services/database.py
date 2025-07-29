from sqlalchemy import inspect
from vpm.database import engine

class DatabaseService:
    """Service for database utility operations."""
    
    @staticmethod
    def get_schemas() -> list[str]:
        """Get all database schemas."""
        inspector = inspect(engine)
        return inspector.get_schema_names()
    
    @staticmethod
    def get_tables() -> list[str]:
        """Get all database tables."""
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()
        tables = []
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                tables.append(table_name)
        return tables
    
    @staticmethod
    def get_columns(table: str, schema: str = "main") -> list[str]:
        """Get all columns for a table."""
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()
        
        if schema not in schemas:
            raise ValueError(f'{schema} is not a valid {engine.url} schema. Run get_schemas() for list of valid schemas.')
        
        tables = DatabaseService.get_tables()
        if table not in tables:
            raise ValueError(f'{table} is not a valid {engine.url} table. Run get_tables() for list of valid tables.')
        
        return [c["name"] for c in inspector.get_columns(table, schema)] 