from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.auth.dependencies import admin_required

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(admin_required)]  # 🔐 ADMIN ONLY
)


# =============================
# GET ALL USERS (ADMIN)
# =============================
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# =============================
# GET SINGLE USER (ADMIN)
# =============================
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# =============================
# UPDATE USER (ADMIN)
# =============================
@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == str(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.email:
        user.email = data.email

    if data.password:
        from app.auth.password import hash_password
        user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return user


# =============================
# DELETE USER (ADMIN)
# =============================
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
