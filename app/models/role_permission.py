from sqlalchemy import Column, String, ForeignKey
from app.database import Base

class RoleHasPermission(Base):
    __tablename__ = "role_has_permissions"

    role_id = Column(String, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(String, ForeignKey("permissions.id"), primary_key=True)
