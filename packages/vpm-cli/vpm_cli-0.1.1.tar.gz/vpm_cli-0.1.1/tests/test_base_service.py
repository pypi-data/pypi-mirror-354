import pytest
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Session
from sqlalchemy import text
from vpm.services.base import BaseService
from vpm.models.base import BaseModel

# Test model for BaseService
class _TestModel(BaseModel, table=True):
    name: str

class _TestService(BaseService[_TestModel]):
    def __init__(self, engine):
        super().__init__(_TestModel, engine=engine)
        self.engine = engine

@pytest.fixture
def test_service(test_engine):
    return _TestService(test_engine)

@pytest.fixture
def test_item():
    return _TestModel(id=uuid4(), name="test_item")

@pytest.fixture(autouse=True)
def clear_test_table(test_engine):
    # Clear the _TestModel table before each test
    with Session(test_engine) as session:
        session.exec(text(f"DELETE FROM {_TestModel.__tablename__}"))
        session.commit()

def test_create(test_service, test_item):
    created_item = test_service.create(test_item)
    assert created_item.id == test_item.id
    assert created_item.name == test_item.name

def test_get_by_id(test_service, test_item):
    # First create the item
    test_service.create(test_item)
    
    # Then retrieve it
    retrieved_item = test_service.get_by_id(test_item.id)
    assert retrieved_item is not None
    assert retrieved_item.id == test_item.id
    assert retrieved_item.name == test_item.name

def test_get_by_name(test_service, test_item):
    # First create the item
    test_service.create(test_item)
    
    # Then retrieve it by name
    retrieved_item = test_service.get_by_name(test_item.name)
    assert retrieved_item is not None
    assert retrieved_item.id == test_item.id
    assert retrieved_item.name == test_item.name

def test_get_all(test_service, test_item):
    # First create the item
    test_service.create(test_item)
    
    # Get all items
    all_items = test_service.get_all()
    assert len(all_items) >= 1
    assert any(item.id == test_item.id for item in all_items)

def test_update(test_service, test_item):
    # First create the item
    test_service.create(test_item)
    
    # Update the item
    new_name = "updated_name"
    updated_item = test_service.update(test_item.id, name=new_name)
    assert updated_item is not None
    assert updated_item.name == new_name

def test_delete(test_service, test_item):
    # First create the item
    test_service.create(test_item)
    
    # Delete the item
    assert test_service.delete(test_item.id) is True
    
    # Verify it's deleted
    assert test_service.get_by_id(test_item.id) is None

def test_get_nonexistent_item(test_service):
    nonexistent_id = uuid4()
    assert test_service.get_by_id(nonexistent_id) is None
    assert test_service.get_by_name("nonexistent_name") is None
    assert test_service.delete(nonexistent_id) is False 