from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.auth import RegisterRequest, LoginRequest
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# Register User (DEFAULT ROLE = user)
# -----------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    # 🔍 Check if user already exists
    user_exists = db.query(User).filter(User.email == data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # 🔑 Fetch DEFAULT role = user (MUST already exist)
    default_role = db.query(Role).filter(Role.name == "user").first()

    if not default_role:
        raise HTTPException(
            status_code=500,
            detail="Default role 'user' not found. Seed roles first."
        )

    # 👤 Create user
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role_id=default_role.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# -----------------------------
# Login User
# -----------------------------
@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
