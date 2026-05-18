"""Seed development data. Run after: alembic upgrade head"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User

ADMIN_PASSWORD = "secret123"


def _is_bcrypt_hash(value: str) -> bool:
    return value.startswith("$2b$") or value.startswith("$2a$")


def seed_admin() -> None:
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            if not _is_bcrypt_hash(admin.password):
                admin.password = hash_password(ADMIN_PASSWORD)
                db.commit()
                print("Updated admin password to bcrypt hash.")
            else:
                print("Admin user already exists — skip.")
            return

        db.add(
            User(
                username="admin",
                email="admin@example.com",
                full_name="Admin User",
                password=hash_password(ADMIN_PASSWORD),
                is_active=True,
            )
        )
        db.commit()
        print(f"Seeded admin user (username: admin, password: {ADMIN_PASSWORD}).")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
