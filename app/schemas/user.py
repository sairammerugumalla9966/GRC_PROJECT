from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ========================
# Base schema
# ========================
class UserBase(BaseModel):
    email: EmailStr


# ========================
# Update schema
# ========================
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# ========================
# Output schema
# ========================
class UserOut(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
