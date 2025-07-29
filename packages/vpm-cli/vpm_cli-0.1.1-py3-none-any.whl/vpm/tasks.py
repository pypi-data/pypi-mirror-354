from typing import Optional
import typer
from uuid import UUID
from vpm.services.elements import TaskService
from vpm.models.tasks import Task, TaskType
from vpm.utils.helpers import serialize
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime, timedelta

app = typer.Typer(no_args_is_help=True)
task_service = TaskService()

@app.command(help="Adds a new task to the local database.")
def add(
    name: Annotated[str, typer.Option(prompt="Task name")],
    type: Annotated[str, typer.Option(prompt="Task type", help="Type of task (MAINTENANCE, REPAIR, REPLACE, INSPECT)")] = "MAINTENANCE",
    description: Annotated[str, typer.Option(prompt="Description")] = None,
    due_date: Annotated[datetime | None, typer.Option()] = None,
    interval: Annotated[int | None, typer.Option(help="Interval for recurring task")] = None,
    interval_unit: Annotated[str | None, typer.Option(help="Unit for interval (days, weeks, months, years)")] = None,
    priority: Annotated[int | None, typer.Option()] = None
) -> None:
    try:
        # Calculate due date if interval is provided
        if interval is not None and interval_unit is not None:
            if interval_unit == "days":
                due_date = datetime.now() + timedelta(days=interval)
            elif interval_unit == "weeks":
                due_date = datetime.now() + timedelta(weeks=interval)
            elif interval_unit == "months":
                # Approximate months as 30 days
                due_date = datetime.now() + timedelta(days=interval * 30)
            elif interval_unit == "years":
                # Approximate years as 365 days
                due_date = datetime.now() + timedelta(days=interval * 365)
            else:
                raise ValueError(f"Invalid interval unit: {interval_unit}. Must be one of: days, weeks, months, years")

        new_task = Task(
            name=name,
            description=description,
            due_date=due_date,
            priority=priority
        )
        task = task_service.create(new_task)
        print(json.dumps(task.model_dump(), indent=4, default=serialize))
    except ValueError:
        print(f"Error: Invalid task type. Must be one of: {', '.join(t.value for t in TaskType)}")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Get task information")
def get(
    name: Annotated[str, typer.Option(prompt="Task name")]
) -> None:
    task = task_service.get_by_name(name=name)
    print(json.dumps(task.model_dump(), indent=4, default=serialize))

@app.command(help="Update task information")
def update(
    name: Annotated[str, typer.Option(prompt="Task name")],
    new_name: Annotated[str | None, typer.Option()] = None,
    type: Annotated[str | None, typer.Option(help="Type of task (MAINTENANCE, REPAIR, REPLACE, INSPECT)")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    due_date: Annotated[datetime | None, typer.Option()] = None,
    priority: Annotated[int | None, typer.Option()] = None
) -> None:
    try:
        task = task_service.get_by_name(name=name)
        args = {k: v for k, v in locals().items() if v is not None and k != 'name'}
        if 'type' in args:
            args['type'] = TaskType(args['type'].upper())
        result = task_service.update(item_id=task.id, **args)
        print(json.dumps(result.model_dump(), indent=4, default=serialize))
    except ValueError:
        print(f"Error: Invalid task type. Must be one of: {', '.join(t.value for t in TaskType)}")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Delete a task")
def delete(
    name: Annotated[str, typer.Option(prompt="Task name")]
) -> None:
    try:
        task = task_service.get_by_name(name=name)
        task_service.delete(item_id=task.id)
        print(f'Task "{name}" deleted successfully')
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Mark a task as complete")
def complete(
    name: Annotated[str, typer.Option(prompt="Task name")]
) -> None:
    try:
        task = task_service.get_by_name(name=name)
        
        # Mark current task as complete
        result = task_service.update(
            item_id=task.id,
            complete=True,
            completed_at=datetime.now()
        )
        print(f'Task "{name}" marked as complete')
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    app() 