import pytest
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from vpm.utils.helpers import (
    utc_now,
    format_decimal,
    parse_decimal,
    serialize,
    to_dict,
    json_serialize,
    next_date,
    validate_str,
    validate_email,
    validate_phone,
    validate_url
)

def test_utc_now():
    """Test that utc_now returns a datetime in UTC timezone."""
    now = utc_now()
    assert isinstance(now, datetime)
    assert now.tzinfo == timezone.utc

def test_format_decimal():
    """Test decimal formatting."""
    assert format_decimal(Decimal('123.456'), 2) == '123.46'
    assert format_decimal(Decimal('123.456'), 0) == '123'
    assert format_decimal(None) == ''

def test_parse_decimal():
    """Test decimal parsing."""
    assert parse_decimal('123.456') == Decimal('123.456')
    assert parse_decimal('invalid') is None
    assert parse_decimal(None) is None

def test_serialize():
    """Test serialization of special types."""
    test_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    test_uuid = UUID('12345678-1234-5678-1234-567812345678')
    
    assert serialize(test_date) == '2024-01-01T00:00:00+00:00'
    assert serialize(test_uuid) == '12345678-1234-5678-1234-567812345678'
    
    with pytest.raises(TypeError):
        serialize(123)  # Should raise TypeError for non-serializable type

def test_to_dict():
    """Test dictionary conversion."""
    test_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    test_decimal = Decimal('123.456')
    
    result = to_dict({
        'date': test_date,
        'decimal': test_decimal,
        'string': 'test'
    })
    
    assert result['date'] == '2024-01-01T00:00:00+00:00'
    assert result['decimal'] == '123.456'
    assert result['string'] == 'test'

def test_json_serialize():
    """Test JSON serialization."""
    test_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    test_decimal = Decimal('123.456')
    
    result = json_serialize({
        'date': test_date,
        'decimal': test_decimal,
        'string': 'test'
    })
    
    assert isinstance(result, str)
    assert '2024-01-01T00:00:00+00:00' in result
    assert '123.456' in result
    assert 'test' in result

def test_next_date():
    """Test next date calculation."""
    test_date = datetime(2024, 1, 1)
    
    # Test yearly
    next_year = next_date('YEARLY', 1, test_date)
    assert next_year.year == 2025
    
    # Test monthly
    next_month = next_date('MONTHLY', 1, test_date)
    assert next_month.month == 2
    
    # Test invalid frequency
    with pytest.raises(ValueError):
        next_date('INVALID', 1, test_date)

def test_validate_str():
    """Test string validation."""
    assert validate_str('  test  ') == 'test'
    assert validate_str('test') == 'test'

def test_validate_email():
    """Test email validation."""
    # Use a real deliverable domain
    assert validate_email('test@gmail.com') == 'test@gmail.com'
    with pytest.raises(ValueError):
        validate_email('invalid-email')

def test_validate_phone():
    """Test phone validation."""
    assert validate_phone('+1234567890') == '+1234567890'
    assert validate_phone('(123) 456-7890') == '1234567890'
    with pytest.raises(ValueError):
        validate_phone('invalid')
    with pytest.raises(ValueError):
        validate_phone('')

def test_validate_url():
    """Test URL validation."""
    assert validate_url('https://example.com') == 'https://example.com'
    assert validate_url('example.com') == 'https://example.com'
    with pytest.raises(ValueError):
        validate_url('invalid')
    with pytest.raises(ValueError):
        validate_url('') 