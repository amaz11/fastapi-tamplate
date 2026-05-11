from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import init_db
from app.middleware.auth_middleware import DemoHeaderMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.add_middleware(DemoHeaderMiddleware)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.on_event("startup")
    def startup_event() -> None:
        init_db()

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "Open /docs for Swagger UI"}

    return app


app = create_app()
