from collections import defaultdict
from time import time

from fastapi import HTTPException, Request, status

_attempts: dict[str, list[float]] = defaultdict(list)


def check_login_rate_limit(request: Request) -> None:
    client = request.client
    key = client.host if client else "unknown"
    now = time()
    window = 60
    max_attempts = 5

    recent = [t for t in _attempts[key] if now - t < window]
    if len(recent) >= max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later.",
        )
    _attempts[key] = [*recent, now]
