import os
import tempfile
import pytest
from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from vpm.models.base import BaseModel
from vpm.models.elements import Element, ElementType
from vpm.models.picklist import Currency, TaskCategory, TaskStatus, DocumentCategory
from vpm.models.tasks import Task
from vpm.models.documents import Document
from vpm.models.parts import Part
from vpm.models.property import Room, Home
from vpm.models.contacts import Contact
from sqlalchemy import select

# Create a temporary SQLite database for testing
@pytest.fixture(scope="session")
def test_db():
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite")
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    os.close(db_fd)
    os.remove(db_path)

@pytest.fixture()
def session(test_db):
    with Session(test_db) as session:
        yield session

def test_base_model(session):
    """Test BaseModel creation and fields."""
    model = BaseModel(name="Test Model", description="Test Description")
    assert model.name == "Test Model"
    assert model.description == "Test Description"
    assert isinstance(model.id, UUID)
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)

def test_home(session):
    """Test Home model creation."""
    home = Home(name="Test Home")
    assert home.name == "Test Home"

def test_room(session):
    """Test Room model creation."""
    room = Room(name="Test Room", level=3)
    assert room.name == "Test Room"
    assert room.level == 3
    
    # Test relationships
    assert isinstance(room.elements, list)

def test_element(session):
    """Test Element model creation and relationships."""
    # Use or create a Home
    home = session.exec(select(Home).limit(1)).first()
    if not home:
        home = Home(name="Test Home", address="123 Main St")
        session.add(home)
        session.commit()
    room = Room(name="Test Room", home_id=home.id)
    session.add(room)
    session.commit()
    element = Element(name="Test Element", room_id=room.id, serial_num="SN123", install_date=datetime.now(timezone.utc))
    session.add(element)
    session.commit()
    # Use session.get() to retrieve the element
    element_from_db = session.get(Element, element.id)
    assert element_from_db.name == "Test Element"
    assert element_from_db.room_id == room.id
    assert element_from_db.serial_num == "SN123"
    assert isinstance(element_from_db.install_date, datetime)
    # SQLite does not preserve tzinfo, so do not check for timezone.utc
    assert element_from_db.room == room

def test_part(session):
    """Test Part model creation and validation."""
    part = Part(name="Test Part", model_number="PN123", cost=Decimal("45.67"), currency="USD")
    assert part.name == "Test Part"
    assert part.model_number == "PN123"
    assert part.cost == Decimal("45.67")
    assert part.currency == "USD"

def test_task(session):
    """Test Task model creation and validation."""
    task = Task(name="Test Task", task_category=TaskCategory.MAINTENANCE, date_due=datetime.now(timezone.utc))
    assert task.name == "Test Task"
    assert task.task_category == TaskCategory.MAINTENANCE
    assert isinstance(task.date_due, datetime)

def test_document(session):
    """Test Document model creation and validation."""
    document = Document(name="Test Document", document_category=DocumentCategory.MANUAL, url="https://example.com/doc")
    assert document.name == "Test Document"
    assert document.document_category == DocumentCategory.MANUAL
    assert document.url == "https://example.com/doc"

def test_contact(session):
    """Test Contact model creation and validation."""
    contact = Contact(email="test@example.com", phone="1234567890")
    assert contact.email == "test@example.com"
    assert contact.phone == "1234567890"

def test_element_type(session):
    """Test ElementType creation and validation."""
    # Test valid creation
    element_type = ElementType(
        name="Test Element",
        brand="Test Brand",
        model="Test Model",
        model_number=123,
        manual_url="https://example.com/manual",
        manufacture_url="https://example.com/manufacture",
        cost=Decimal("100.50"),
        currency="USD"
    )
    assert element_type.name == "Test Element"
    assert element_type.brand == "Test Brand"
    assert element_type.model == "Test Model"
    assert element_type.model_number == 123
    assert element_type.manual_url == "https://example.com/manual"
    assert element_type.manufacture_url == "https://example.com/manufacture"
    assert element_type.cost == Decimal("100.50")
    assert element_type.currency == "USD"

    # Test currency validation
    with pytest.raises(ValueError):
        ElementType(currency="INVALID")

    # Test URL validation
    with pytest.raises(ValueError):
        ElementType(manual_url="invalid-url") 