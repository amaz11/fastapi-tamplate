from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import check_db_connection

router = APIRouter(tags=["health"])


@router.get("/health", response_model=None)
def health_check() -> dict[str, str] | JSONResponse:
    db_ok = check_db_connection()
    body = {
        "status": "ok" if db_ok else "degraded",
        "app": settings.app_name,
        "database": "ok" if db_ok else "unavailable",
    }
    if not db_ok:
        return JSONResponse(status_code=503, content=body)
    return body
