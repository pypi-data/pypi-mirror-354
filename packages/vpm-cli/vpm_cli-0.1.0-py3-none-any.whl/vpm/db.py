import typer
from typing_extensions import Annotated
from rich import print
from vpm.database.init import init_db
from vpm.database.config import engine
from vpm.services.database import DatabaseService

app = typer.Typer(no_args_is_help=True)

database_service = DatabaseService()

@app.command()
def create(overwrite: Annotated[bool, typer.Option("--overwrite", prompt="Overwrite existing DB?")] = False):
    """Initializes the database and creates all necessary tables."""
    try:
        db_url = init_db(overwrite=overwrite)
        print(db_url)
    except FileExistsError as e:
        print(e)

@app.command()
def info():
    """Prints the database engine configuration (including URL)."""
    print(engine)

@app.command()
def schemas():
    """Prints the schemas in the database."""
    print(database_service.get_schemas())

@app.command()
def tables():
    """Prints the tables in the database."""
    print(database_service.get_tables())

@app.command()
def columns(table: str):
    """Prints the columns of a table."""
    print(database_service.get_columns(table))

if __name__ == "__main__":
    app() 