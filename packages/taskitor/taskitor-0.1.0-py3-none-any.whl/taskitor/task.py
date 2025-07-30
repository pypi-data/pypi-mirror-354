from datetime import datetime



class Task:
    def __init__(self, id, description, status="to-do", created_at=None, updated_at=None):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or self.created_at

    STATUS_TODO = "to-do"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_DONE = "done"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            description=data["description"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )