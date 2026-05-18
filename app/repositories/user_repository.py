from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate


class UserRepository(BaseRepository):
    db: Session

    def count_users(self) -> int:
        return self.db.query(User).count()

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).order_by(User.id).offset(skip).limit(limit).all()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, payload: UserCreate, password_hash: str) -> User:
        user = User(
            username=payload.username,
            email=payload.email,
            full_name=payload.full_name,
            password=password_hash,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
