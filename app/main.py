import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.middleware.auth_middleware import DemoHeaderMiddleware
from app.middleware.request_id import RequestIdMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting %s", settings.app_name)
    yield
    engine.dispose()
    logger.info("Shut down %s", settings.app_name)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    app.add_middleware(RequestIdMiddleware)
    if settings.enable_demo_middleware:
        app.add_middleware(DemoHeaderMiddleware)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "Open /docs for Swagger UI"}

    return app


app = create_app()
