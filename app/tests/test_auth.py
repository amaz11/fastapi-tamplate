from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_returns_token() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secret123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
