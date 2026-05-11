from fastapi import HTTPException, status

from app.core.config import settings


def create_demo_token(username: str) -> str:
    """Very small demo token. Good for learning, bad for production."""

    return f"{username}:{settings.fake_secret_key}"


def verify_demo_token(token: str) -> str:
    """Return username if token format is valid."""

    if ":" not in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )

    username, secret = token.split(":", maxsplit=1)
    if secret != settings.fake_secret_key or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return username
