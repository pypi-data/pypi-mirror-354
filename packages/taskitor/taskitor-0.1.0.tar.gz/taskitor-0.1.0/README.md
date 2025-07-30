# Taskitor CLI – Task Tracker

## English

Taskitor is a simple command-line application for managing tasks. Each task is stored in `tasks.json` with one of three statuses: `to-do`, `in-progress` or `done`.

### Usage

Install Taskitor from PyPI and run it from anywhere:

```bash
pip install taskitor
taskitor <command> [arguments]
```

#### Commands
- `add "description"` – add a new task.
- `delete <id>` – remove a task by its ID.
- `update <id> "new description"` – modify the description of a task.
- `status <id> <status>` – change the task status to `to-do`, `in-progress`, or `done`.
- `list [status]` – list all tasks, optionally filtering by status.

---

## Español

Taskitor es una aplicación de línea de comandos para gestionar tareas. Las tareas se guardan en `tasks.json` y pueden estar en los estados `to-do`, `in-progress` o `done`.

### Uso

Instala Taskitor desde PyPI y ejecútalo desde cualquier ruta:

```bash
pip install taskitor
taskitor <comando> [argumentos]
```

#### Comandos
- `add "descripcion"` – agrega una nueva tarea.
- `delete <id>` – elimina una tarea por su ID.
- `update <id> "nueva descripcion"` – modifica la descripción de una tarea.
- `status <id> <estado>` – cambia el estado de la tarea a `to-do`, `in-progress` o `done`.
- `list [estado]` – muestra todas las tareas, con la opción de filtrar por estado.

---

Este proyecto nace de la inspiración obtenida en [roadmap.sh](https://roadmap.sh/projects/task-tracker), a quienes agradezco por sus valiosos contenidos.

---
