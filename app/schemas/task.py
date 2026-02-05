from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =====================
# Base schema
# =====================
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# =====================
# Create task
# =====================
class TaskCreate(TaskBase):
    pass


# =====================
# Update task (THIS FIXES YOUR ERROR)
# =====================
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# =====================
# Response schema
# =====================
class TaskOut(TaskBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True   # ✅ Pydantic v2
