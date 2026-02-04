from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"

class TaskOut(TaskCreate):
    id: str
    owner_id: str
    created_at: str
    updated_at: str
