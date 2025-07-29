from datetime import datetime, timezone
from typing import Any, Dict, Optional
from decimal import Decimal
import json
from uuid import UUID
from email_validator import validate_email as validate_email_address, EmailNotValidError
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY
import re
import decimal

def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)

def format_decimal(value: Optional[Decimal], places: int = 2) -> str:
    """Format decimal value with specified number of decimal places."""
    if value is None:
        return ""
    return f"{value:.{places}f}"

def parse_decimal(value: str) -> Optional[Decimal]:
    """Parse string to Decimal, return None if invalid."""
    if not value:
        return None
    try:
        return Decimal(str(value))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return None

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def to_dict(obj: Any) -> Any:
    """Convert object to dictionary, handling special types recursively."""
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_dict(i) for i in obj]
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, UUID):
        return str(obj)
    if hasattr(obj, "__dict__"):
        return to_dict(obj.__dict__)
    return obj

def json_serialize(obj: Any) -> str:
    """Serialize object to JSON string."""
    return json.dumps(to_dict(obj), indent=2)

def next_date(freq: str, interval: int, dt: datetime = None) -> datetime:
    """Calculate the next date based on frequency and interval."""
    if dt is None:
        dt = datetime.now()
        
    if freq.upper() not in ["YEARLY", "MONTHLY", "WEEKLY", "DAILY"]:
        raise ValueError(f'{freq.upper()} must be one of YEARLY, MONTHLY, WEEKLY, DAILY')
        
    return rrule(freq=eval(freq.upper()), interval=interval, dtstart=dt)[1] 

# validator functions
def validate_str(value: str) -> str:
    """Validate string."""
    return value.strip()

def validate_email(value: str) -> str:
    """Validate email."""
    try:
        validate_email_address(value, check_deliverability=True)
        return value
    except EmailNotValidError as e:
        raise ValueError(f"Invalid email: {e}")
    
def validate_phone(value: str) -> str:
    """Validate phone."""
    if not value:
        raise ValueError("Phone is required")
    # Normalize: remove all non-digit except leading +
    value = re.sub(r'[^\d+]', '', value)
    if value.startswith('+'):
        digits = value[1:]
    else:
        digits = value
    if not digits.isdigit() or not (4 <= len(digits) <= 19):
        raise ValueError("Invalid phone number")
    return value

def validate_url(value: str) -> str:
    """Validate URL."""
    if not value:
        raise ValueError("URL is required")
    if not value.startswith(('http://', 'https://')):
        value = f"https://{value}"
    # Stricter regex: require at least one dot and a valid TLD-like ending, and at least one character before the dot
    if not re.match(r"^https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(/.*)?$", value):
        raise ValueError("Invalid URL")
    return value    