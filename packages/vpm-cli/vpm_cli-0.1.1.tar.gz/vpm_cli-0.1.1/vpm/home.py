from typing import Optional
import typer
from uuid import UUID
from vpm.services.property import HomeService
from vpm.services.elements import ElementService
from vpm.models.property import Home
from vpm.models.elements import Element
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime
from vpm.utils.helpers import serialize

app = typer.Typer(no_args_is_help=True)
home_service = HomeService()
element_service = ElementService()

@app.command(help="Adds a home to the local database")
def add(
    name: Annotated[str, typer.Option(prompt="Unique name")], 
    address: Annotated[str, typer.Option(prompt="Street address")],
    description: Annotated[str, typer.Option(prompt="Description")] = ""
    ) -> None:
    try:
        new_home = Home(name=name, address=address, description=description)
        home = home_service.create(new_home)
        print(json.dumps(home.model_dump(), indent=4, default=serialize))
    except Exception as e:
        print(e)

@app.command(help="Get home information")
def get() -> None:
    home = home_service.get()
    print(json.dumps(home.model_dump(), indent=4, default=serialize))

@app.command(help="Update home information")
def update(
    name: Annotated[str | None, typer.Option()] = None, 
    address: Annotated[str | None, typer.Option()] = None) -> None:
    home_id = home_service.get().id
    args = {k: v for k, v in locals().items() if v is not None and k != 'home_id'}
    r = home_service.update(
        item_id=home_id,
        **args
        )
    print(r)

@app.command(help="Delete home")
def delete() -> None:
    home_id = home_service.get().id
    print(home_id)
    try:
        home_service.delete(item_id=home_id)
        print('Home deleted')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app()