from sqlmodel import create_engine
from pathlib import Path
from vpm.config.settings import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

def get_engine():
    """Get the database engine instance."""
    return engine 