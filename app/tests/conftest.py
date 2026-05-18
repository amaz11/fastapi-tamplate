import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")
os.environ.setdefault("ENABLE_DEMO_MIDDLEWARE", "false")

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient

from alembic import command
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def prepare_database() -> None:
    if os.path.exists("test.db"):
        os.remove("test.db")
    command.upgrade(Config("alembic.ini"), "head")

    from scripts.seed import seed_admin

    seed_admin()
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def admin_token(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secret123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
