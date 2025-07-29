from sqlmodel import SQLModel, create_engine
from sqlalchemy import inspect, text
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

def init_db():
    """Initialize the database by creating all tables."""
    SQLModel.metadata.create_all(engine) 