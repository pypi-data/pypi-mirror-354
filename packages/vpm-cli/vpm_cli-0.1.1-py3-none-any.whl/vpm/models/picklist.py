from enum import Enum

class DocumentCategory(Enum):
    """Category of document."""
    WARRANTY = "WARRANTY"
    MANUAL = "MANUAL"
    CONTRACT = "CONTRACT"
    OTHER = "OTHER"

class TaskCategory(str, Enum):
    """Category of task."""
    INSPECTION = "Inspection"
    INSTALLATION = "Installation"
    MAINTENANCE = "Maintenance"
    REMOVAL = "Removal"
    RENOVATION = "Renovation"

class TaskStatus(str, Enum):
    """Status of task."""
    NOT_YET_STARTED = "NOT_YET_STARTED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"

class IntervalUnit(str, Enum):
    """Unit of interval."""
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"

class Currency(str,Enum):
    """Currency of element."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"


