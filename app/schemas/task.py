from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------
# Request schema (Create Task)
# -----------------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"


# -----------------------------
# Response schema (Task Output)
# -----------------------------
class TaskOut(TaskCreate):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # REQUIRED for SQLAlchemy ORM
