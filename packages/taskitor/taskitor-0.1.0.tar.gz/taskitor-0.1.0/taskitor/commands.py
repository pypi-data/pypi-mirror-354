from taskitor.task import Task
from taskitor.storage import load_tasks, save_tasks
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console(highlight=False)


def normalize_status(status: str) -> str | None:
    """Return the canonical status name regardless of input case.

    Accepts both new hyphenated status names and legacy names with spaces.
    """
    status_map = {
        Task.STATUS_TODO.lower(): Task.STATUS_TODO,
        Task.STATUS_IN_PROGRESS.lower(): Task.STATUS_IN_PROGRESS,
        Task.STATUS_DONE.lower(): Task.STATUS_DONE,
        "to do": Task.STATUS_TODO,
        "in progress": Task.STATUS_IN_PROGRESS,
    }
    return status_map.get(status.lower())


def add_task(description):
    tasks = load_tasks()
    if not tasks:
        id = 1
    else:
        id = max([t.id for t in tasks]) + 1

    new_task = Task(id, description)

    tasks.append(new_task)
    save_tasks(tasks)

    console.print(f"Task added successfully (ID: {id})", style="bold bright_cyan")

def delete_task(id: int):
    tasks = load_tasks()
    task_to_rid = None

    for t in tasks:
        if t.id == id:
            task_to_rid = t

    if task_to_rid:
        tasks.remove(task_to_rid)
        save_tasks(tasks)
        console.print(f"Task with ID: {id} deleted successfully", style="bold bright_cyan")
    else:
        console.print(f"Task with ID: {id} not found", style="bold bright_red")

def update_task(id: int, description: str):
    tasks = load_tasks()
    task_to_update = None

    for t in tasks:
        if t.id == id:
            task_to_update = t

    if task_to_update:
        task_to_update.description = description
        task_to_update.updated_at = datetime.now().isoformat()
        save_tasks(tasks)
        console.print(f"Task with ID: {id} updated successfully", style="bold bright_cyan")
    else:
        console.print(f"Task with ID: {id} not found", style="bold bright_red")

def change_status(id: int, status: str):
    status_normalized = normalize_status(status)
    if status_normalized:

        tasks = load_tasks()
        task_to_update = None

        for t in tasks:
            if t.id == id:
                task_to_update = t

        if task_to_update:
            task_to_update.status = status_normalized
            task_to_update.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            console.print(
                f"Task with ID: {id} marked as {status_normalized} successfully",
                style="bold bright_cyan",
            )
        else:
            console.print(f"Task with ID: {id} not found", style="bold bright_red")

    else:
        console.print(
            f"Invalid status: {status}. Valid statuses are: to-do, in-progress, done",
            style="bold bright_red",
        )

def list_tasks(status: str | None = None):
    tasks = load_tasks()

    status_normalized = normalize_status(status) if status else None

    if status and not status_normalized:
        console.print(
            f"Invalid status: {status}. Valid statuses are: to-do, in-progress, done",
            style="bold bright_red",
        )
        return

    if status_normalized:
        tasks = [t for t in tasks if t.status == status_normalized]
        console.print(
            f"Tasks with status '{status_normalized}':",
            style="bold bright_magenta",
        )
    else:
        console.print("All tasks:", style="bold bright_magenta")

    if not tasks:
        console.print("No tasks found.", style="bright_yellow")
        return

    table = Table(show_header=True, header_style="bold bright_blue")
    table.add_column("ID", style="bright_white")
    table.add_column("Description", style="bright_white")
    table.add_column("Status", style="bright_white")
    table.add_column("Created", style="bright_white")
    table.add_column("Updated", style="bright_white")

    status_colors = {
        Task.STATUS_TODO: "bright_magenta",
        Task.STATUS_IN_PROGRESS: "bright_yellow",
        Task.STATUS_DONE: "bright_green",
    }

    for t in tasks:
        table.add_row(
            str(t.id),
            t.description,
            f"[{status_colors.get(t.status, 'white')}]" + t.status + "[/]",
            t.created_at.split("T")[0],
            t.updated_at.split("T")[0],
        )

    console.print(table)

