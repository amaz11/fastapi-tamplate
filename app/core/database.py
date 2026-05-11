from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

DATABASE_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": settings.database_url,
    "SQLALCHEMY_TRACK_MODIFICATIONS": settings.database_track_modifications,
}

connect_args = (
    {"check_same_thread": False}
    if DATABASE_CONFIG["SQLALCHEMY_DATABASE_URI"].startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_CONFIG["SQLALCHEMY_DATABASE_URI"],
    connect_args=connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models.user import User

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            db.add(
                User(
                    username="admin",
                    email="admin@example.com",
                    full_name="Admin User",
                    password="secret123",
                    is_active=True,
                )
            )
            db.commit()
    finally:
        db.close()
