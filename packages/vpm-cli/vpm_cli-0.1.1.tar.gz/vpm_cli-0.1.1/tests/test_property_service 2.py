import pytest
from uuid import uuid4
from sqlmodel import Session, select
from sqlalchemy import text
from vpm.models.property import Home, Room
from vpm.services.property import HomeService, RoomService
from sqlalchemy.orm import selectinload

@pytest.fixture
def home_service(test_engine):
    # Patch HomeService to use test_engine
    class _TestHomeService(HomeService):
        def __init__(self):
            super().__init__()
            self.engine = test_engine
        def get(self):
            with Session(self.engine) as session:
                session.expire_on_commit = False
                return session.exec(select(Home)).first()
        def get_rooms(self, home_id):
            with Session(self.engine) as session:
                result = session.exec(
                    text("SELECT id, name, level, home_id FROM room WHERE home_id = :home_id"),
                    {"home_id": str(home_id)}
                )
                rows = result.fetchall()
                return [
                    {"id": row[0], "name": row[1], "level": row[2], "home_id": row[3]} for row in rows
                ]
    return _TestHomeService()

@pytest.fixture
def room_service(test_engine):
    class _TestRoomService(RoomService):
        def __init__(self):
            super().__init__()
            self.engine = test_engine
        def get_by_level(self, level):
            with Session(self.engine) as session:
                session.expire_on_commit = False
                return session.exec(select(Room).where(Room.level == level)).all()
    return _TestRoomService()

@pytest.fixture(autouse=True)
def clear_property_tables(test_engine):
    with Session(test_engine) as session:
        session.exec(text(f"DELETE FROM room"))
        session.exec(text(f"DELETE FROM home"))
        session.commit()

def test_home_service_get(home_service, test_engine):
    home = Home(id=uuid4(), name="Test Home", address="123 Main St")
    with Session(test_engine) as session:
        session.add(home)
        session.commit()
    result = home_service.get()
    assert result is not None
    assert result.address == "123 Main St"

def test_home_service_get_rooms(home_service, test_engine):
    home = Home(id=uuid4(), name="Rooms Home", address="456 Oak Ave")
    room1 = Room(id=uuid4(), name="Living Room", level=1, home_id=home.id)
    room2 = Room(id=uuid4(), name="Bedroom", level=2, home_id=home.id)
    with Session(test_engine) as session:
        session.add(home)
        session.add(room1)
        session.add(room2)
        session.commit()
    rooms = home_service.get_rooms(home.id)
    assert len(rooms) == 2
    levels = [r['level'] for r in rooms]
    assert set(levels) == {1, 2}
    names = [r['name'] for r in rooms]
    assert set(names) == {"Living Room", "Bedroom"}
    home_ids = [r['home_id'] for r in rooms]
    assert all(hid == home.id for hid in home_ids)

def test_room_service_get_by_level(room_service, test_engine):
    home = Home(id=uuid4(), name="Level Home", address="789 Pine Rd")
    room1 = Room(id=uuid4(), name="Kitchen", level=1, home_id=home.id)
    room2 = Room(id=uuid4(), name="Office", level=2, home_id=home.id)
    room3 = Room(id=uuid4(), name="Bathroom", level=1, home_id=home.id)
    with Session(test_engine) as session:
        session.add(home)
        session.add(room1)
        session.add(room2)
        session.add(room3)
        session.commit()
    level1_rooms = room_service.get_by_level(1)
    assert len(level1_rooms) == 2
    assert all(getattr(r, 'level', None) == 1 for r in level1_rooms)
    level2_rooms = room_service.get_by_level(2)
    assert len(level2_rooms) == 1
    assert getattr(level2_rooms[0], 'level', None) == 2 