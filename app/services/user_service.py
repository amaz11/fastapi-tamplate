from app.models.user import User
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """Business rules live here, not in route functions."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list_users(self) -> list[User]:
        return self.repository.list_users()

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.repository.get_by_username(payload.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        return self.repository.create_user(payload)
