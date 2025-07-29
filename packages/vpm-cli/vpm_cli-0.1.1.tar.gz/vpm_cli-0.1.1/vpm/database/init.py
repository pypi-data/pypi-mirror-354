from sqlmodel import SQLModel
from sqlalchemy import text
import os
from pathlib import Path
from vpm.database.config import engine
from vpm.config.settings import settings

def create_home_trigger():
    """Create trigger to ensure only one row exists in the home table."""
    # First drop the trigger if it exists
    drop_trigger_sql = "DROP TRIGGER IF EXISTS single_row_check;"
    
    trigger_sql = """
    CREATE TRIGGER single_row_check
        BEFORE INSERT ON home
        WHEN (SELECT COUNT(*) FROM home) >= 1
        BEGIN
            SELECT RAISE(ABORT, 'Only one row allowed in home table. Use update to update home information.');
        END;
    """
    try:
        with engine.connect() as connection:
            # Drop existing trigger
            connection.execute(text(drop_trigger_sql))
            # Create new trigger
            connection.execute(text(trigger_sql))
            connection.commit()
    except Exception as e:
        raise

def init_db(overwrite: bool = False) -> str:
    """Initialize the database and create all tables."""
    db_path = settings.get_database_path()
    
    if db_path.exists() and overwrite:
        try:
            os.remove(db_path)
        except Exception as e:
            raise e
    
    if db_path.exists() and not overwrite:
        raise FileExistsError(
            f'Database already exists at {db_path}. To overwrite include `--overwrite`'
        )
    
    # Ensure app directory exists
    settings.ensure_data_directory()
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Create triggers
    create_home_trigger()
    
    return str(db_path) 