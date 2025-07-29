from typing import Optional
import typer
from uuid import UUID
from vpm.services.parts import PartService
from vpm.models.parts import Part
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime
from vpm.utils.helpers import serialize

app = typer.Typer(no_args_is_help=True)
part_service = PartService()

@app.command(help="Adds a new part to the local database.")
def add(
    name: Annotated[str, typer.Option(prompt="Part name")],
    description: Annotated[str, typer.Option(prompt="Description")],
    manufacturer: Annotated[str | None, typer.Option()] = None,
    model_number: Annotated[str | None, typer.Option()] = None,
    serial_number: Annotated[str | None, typer.Option()] = None
) -> None:
    try:
        new_part = Part(
            name=name,
            description=description,
            manufacturer=manufacturer,
            model_number=model_number,
            serial_number=serial_number
        )
        part = part_service.create(new_part)
        print(json.dumps(part.model_dump(), indent=4, default=serialize))
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Get part information")
def get(
    name: Annotated[str, typer.Option(prompt="Part name")]
) -> None:
    part = part_service.get_by_name(name=name)
    print(json.dumps(part.model_dump(), indent=4, default=serialize))

@app.command(help="Update part information")
def update(
    name: Annotated[str, typer.Option(prompt="Part name")],
    new_name: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    manufacturer: Annotated[str | None, typer.Option()] = None,
    model_number: Annotated[str | None, typer.Option()] = None,
    serial_number: Annotated[str | None, typer.Option()] = None
) -> None:
    part = part_service.get_by_name(name=name)
    args = {k: v for k, v in locals().items() if v is not None and k != 'name'}
    result = part_service.update(item_id=part.id, **args)
    print(json.dumps(result.model_dump(), indent=4, default=serialize))

@app.command(help="Delete a part")
def delete(
    name: Annotated[str, typer.Option(prompt="Part name")]
) -> None:
    try:
        part = part_service.get_by_name(name=name)
        part_service.delete(item_id=part.id)
        print(f'Part "{name}" deleted successfully')
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    app() 