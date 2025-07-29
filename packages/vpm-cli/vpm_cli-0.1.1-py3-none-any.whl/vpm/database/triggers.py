from sqlalchemy import text
from vpm.database.engine import engine

def create_home_trigger():
    """Create trigger to ensure only one row exists in the home table."""
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
            connection.execute(text(trigger_sql))
            connection.commit()
    except Exception as e:
        raise e 