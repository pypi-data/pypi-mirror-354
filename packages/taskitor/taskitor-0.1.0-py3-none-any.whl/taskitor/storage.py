import json
import os
from taskitor.task import Task

FILE_PATH = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []
    
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
        return [Task.from_dict(t) for t in data]
    
def save_tasks(tasks):
    with open(FILE_PATH, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4)