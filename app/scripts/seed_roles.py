import os
import sys
import uuid
from datetime import datetime

# Add parent folder to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.role import Role
from app.models.user import User
from app.auth.password import hash_password

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_roles_and_admin():
    db: Session = SessionLocal()

    try:
        # ----------------------------
        # 1️⃣ Seed Roles
        # ----------------------------
        roles = ["ADMIN", "USER"]
        for role_name in roles:
            role_exists = db.query(Role).filter(Role.name == role_name).first()
            if not role_exists:
                new_role = Role(
                    id=str(uuid.uuid4()),
                    name=role_name
                )
                db.add(new_role)
        db.commit()

        # ----------------------------
        # 2️⃣ Create initial admin user
        # ----------------------------
        admin_email = "admin@example.com"
        admin_password = "Admin@123"  # You can change this
        admin_exists = db.query(User).filter(User.email == admin_email).first()
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()

        if not admin_exists:
            admin_user = User(
                id=str(uuid.uuid4()),
                email=admin_email,
                hashed_password=hash_password(admin_password),
                role_id=admin_role.id,
                created_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()
            print(f"✅ Admin user created: {admin_email} / {admin_password}")
        else:
            print(f"ℹ️ Admin user already exists: {admin_email}")

        print("✅ Roles seeded successfully!")

    except Exception as e:
        print("❌ Error seeding roles/admin:", str(e))
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_roles_and_admin()
