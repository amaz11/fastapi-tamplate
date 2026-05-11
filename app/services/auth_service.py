from fastapi import HTTPException, status

from app.core.security import create_demo_token
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def login(self, username: str, password: str) -> str:
        user = self.repository.get_by_username(username)
        if not user or user.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return create_demo_token(username)
