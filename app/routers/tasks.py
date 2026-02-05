from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.auth.dependencies import get_current_user, admin_required
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -----------------------------
# GET all tasks (admin-only)
# -----------------------------
@router.get("/", response_model=List[TaskOut])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),  # 🔐 Admin only
):
    tasks = db.query(Task).all()
    return tasks


# -----------------------------
# GET my tasks (normal user)
# -----------------------------
@router.get("/me", response_model=List[TaskOut])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Task).filter(Task.owner_id == current_user.id).all()


# -----------------------------
# GET single task
# -----------------------------
@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only admin or owner can access
    if task.owner_id != current_user.id and current_user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return task


# -----------------------------
# CREATE task
# -----------------------------
@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=current_user.id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# -----------------------------
# UPDATE task
# -----------------------------
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only owner or admin can update
    if task.owner_id != current_user.id and current_user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update this task",
        )

    # Update fields dynamically
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


# -----------------------------
# DELETE task
# -----------------------------
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == str(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only owner or admin can delete
    if task.owner_id != current_user.id and current_user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete this task",
        )

    db.delete(task)
    db.commit()
    return None
