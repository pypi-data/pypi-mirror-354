import os
from pathlib import Path
from typing import Optional
import typer

class Settings:
    """Configuration settings for the VPM application."""
    
    # Base paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    APP_DIR: Path = Path(typer.get_app_dir("vpm"))
    
    # Database settings
    DATABASE_URL: str = os.getenv("VPM_DATABASE_URL", f"sqlite:///{APP_DIR}/vpm.db")
    
    # Application settings
    DEBUG: bool = os.getenv("VPM_DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("VPM_LOG_LEVEL", "INFO")
    
    # API settings
    API_HOST: str = os.getenv("VPM_API_HOST", "localhost")
    API_PORT: int = int(os.getenv("VPM_API_PORT", "8000"))
    
    @classmethod
    def get_database_path(cls) -> Path:
        """Get the database file path."""
        return cls.APP_DIR / "vpm.db"
    
    @classmethod
    def ensure_data_directory(cls) -> None:
        """Ensure the application directory exists."""
        cls.APP_DIR.mkdir(parents=True, exist_ok=True)

# Create a global settings instance
settings = Settings() 