import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def _error_body(detail: object, code: str) -> dict[str, object]:
    return {"detail": detail, "code": code}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        code = exc.headers.get("X-Error-Code") if exc.headers else None
        if not code:
            code = f"http_{exc.status_code}"
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.detail, code),
            headers={k: v for k, v in (exc.headers or {}).items() if k != "X-Error-Code"},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_body(exc.errors(), "validation_error"),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=_error_body("Internal server error", "internal_error"),
        )
