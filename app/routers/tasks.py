from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut
from app.auth.jwt import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -----------------------------
# Create Task
# -----------------------------
@router.post("/", response_model=TaskOut)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        owner_id=current_user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# -----------------------------
# List Tasks (filter + pagination)
# -----------------------------
@router.get("/", response_model=List[TaskOut])
def list_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    offset = (page - 1) * limit
    tasks = query.offset(offset).limit(limit).all()

    return tasks


# -----------------------------
# Get Single Task
# -----------------------------
@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return task


# -----------------------------
# Update Task
# -----------------------------
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: str,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    task.title = data.title
    task.description = data.description
    task.status = data.status
    task.priority = data.priority

    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# Delete Task
# -----------------------------
@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(task)
    db.commit()

    return None
