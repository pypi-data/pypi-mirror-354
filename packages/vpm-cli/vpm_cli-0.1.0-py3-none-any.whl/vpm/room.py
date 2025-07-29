import typer
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID
from rich import print
from vpm.services.property import RoomService, HomeService
from vpm.services.elements import ElementService
from vpm.models.property import Room
from vpm.models.elements import Element

app = typer.Typer(no_args_is_help=True)
room_service = RoomService()
element_service = ElementService()
home_service = HomeService()

@app.command()
def add(
    name: Annotated[str, typer.Option(prompt="Room name")],
    level: Annotated[int, typer.Option(prompt="Level")] = 0,
    description: Annotated[str, typer.Option(prompt="Description")] = ""
    ):
    try:
        home_id = home_service.get().id
        new_room = Room(name=name, home_id=home_id, level=level, description=description)
        room = room_service.create(new_room)
    except Exception as e:
        print(e)
    print(room)

@app.command()
def all() -> None:
    room = room_service.get_all()
    print(room)

@app.command()
def get_by_name(
    name: Annotated[str, typer.Option(prompt="Name")]
    ) -> None:
    room = room_service.get_by_name(name=name)
    print(room)

@app.command()
def update(
    name: Annotated[str, typer.Option(prompt="Room Name")] = None
    ):
    room_id = room_service.get_by_name(name=name).id
    args = {k: v for k, v in locals().items() if v is not None and k != 'room_id'}
    r = room_service.update(
        item_id=room_id,
        **args
        )
    print(r)

@app.command()
def delete(name: Annotated[str, typer.Option(prompt="Room name")]) -> None:
    room_id = room_service.get_by_name(name=name).id
    room_service.delete(id=room_id)

if __name__ == "__main__":
    app()