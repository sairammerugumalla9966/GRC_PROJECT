from fastapi import Depends, HTTPException, status
from app.auth.jwt import get_current_user
from app.models.user import User


def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.role or current_user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
