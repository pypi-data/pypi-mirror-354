from typing import Optional
import typer
from uuid import UUID
from vpm.services.elements import ElementService
from vpm.services.property import RoomService
from vpm.models.elements import Element
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime
from vpm.utils.helpers import serialize

app = typer.Typer(no_args_is_help=True)
element_service = ElementService()
room_service = RoomService()

@app.command(help="Adds a new element to the local database.")
def add(
    room_name: Annotated[str, typer.Option(prompt="Room name")],
    name: Annotated[str, typer.Option(prompt="Element name")],
    description: Annotated[str, typer.Option(prompt="Description")] = "",
    brand: Annotated[str, typer.Option(prompt="Brand")] = "",
    model: Annotated[str, typer.Option(prompt="Model")] = "",
    model_number: Annotated[str, typer.Option(prompt="Model number")] = "",
    manual_url: Annotated[str, typer.Option(prompt="Manual URL")] = "",
    manufacture_url: Annotated[str, typer.Option(prompt="Manufacture URL")] = "",
    install_date: Annotated[datetime, typer.Option(prompt="Install date")] = None,
    cost: Annotated[float, typer.Option(prompt="Cost")] = None,
    currency: Annotated[str, typer.Option(prompt="Currency")] = "USD"
) -> None:
    try:
        room_id = room_service.get_by_name(name=room_name).id
        new_element = Element(
            room_id=room_id, 
            name=name, 
            description=description, 
            brand=brand,
            model=model,
            model_number=model_number,
            manual_url=manual_url,
            manufacture_url=manufacture_url,
            install_date=install_date,
            cost=cost,
            currency=currency
        )
        element = element_service.create(new_element)
        print(json.dumps(element.model_dump(), indent=4, default=serialize))
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Get element information")
def get(
    name: Annotated[str, typer.Option(prompt="Element name")]
) -> None:
    element = element_service.get_by_name(name=name)
    print(json.dumps(element.model_dump(), indent=4, default=serialize))

@app.command(help="Get all elements")
def all():
    elements = element_service.get_all()
    print(json.dumps([element.model_dump() for element in elements], indent=4, default=serialize))

@app.command(help="Update element information")
def update(
    name: Annotated[str, typer.Option(prompt="Element name")],
    new_name: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None
) -> None:
    element = element_service.get_by_name(name=name)
    args = {k: v for k, v in locals().items() if v is not None and k != 'name'}
    result = element_service.update(element_id=element.id, **args)
    print(json.dumps(result.model_dump(), indent=4, default=serialize))

@app.command(help="Delete an element")
def delete(
    name: Annotated[str, typer.Option(prompt="Element name")]
) -> None:
    try:
        element = element_service.get_by_name(name=name)
        element_service.delete(item_id=element.id)
        print(f'Element "{name}" deleted successfully')
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    app() 