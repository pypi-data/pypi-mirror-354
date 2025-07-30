import sys
from taskitor.commands import (
    add_task,
    delete_task,
    update_task,
    change_status,
    list_tasks,
    console,
)

def main():
    if len(sys.argv) < 2:
        console.print(
            "Please provide a command: add, delete, update, change_status, list",
            style="bright_yellow",
        )
        return
    
    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            console.print("Usage: add \"description\"", style="bright_yellow")
            return
        description = sys.argv[2]
        add_task(description)

    elif command == "delete":
        if len(sys.argv) < 3:
            console.print("Usage: delete <id>", style="bright_yellow")
            return
        delete_task(int(sys.argv[2]))

    elif command == "update":
        if len(sys.argv) < 4:
            console.print(
                "Usage: update <id> \"new description\"",
                style="bright_yellow",
            )
            return
        update_task(int(sys.argv[2]), sys.argv[3])

    elif command == "status":
        if len(sys.argv) < 4:
            console.print("Usage: status <id> <status>", style="bright_yellow")
            return
        change_status(int(sys.argv[2]), sys.argv[3])

    elif command == "list":
        status = sys.argv[2] if len(sys.argv) >= 3 else None
        list_tasks(status)

    else:
        console.print(f"Unknown command: {command}", style="bold bright_red")

if __name__ == "__main__":
    main()
