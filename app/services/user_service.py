from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """Business rules live here, not in route functions."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list_users(self, page: int = 1, page_size: int = 20) -> tuple[list[User], int]:
        skip = (page - 1) * page_size
        users = self.repository.list_users(skip=skip, limit=page_size)
        total = self.repository.count_users()
        return users, total

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.repository.get_by_username(payload.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        password_hash = hash_password(payload.password)
        return self.repository.create_user(payload, password_hash=password_hash)
