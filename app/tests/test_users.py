from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_users() -> None:
    response = client.get("/api/v1/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
