from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def login(self, username: str, password: str) -> str:
        user = self.repository.get_by_username(username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        return create_access_token(user.username)
