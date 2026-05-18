from fastapi.testclient import TestClient


def test_login_returns_jwt(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["access_token"].count(".") == 2


def test_login_wrong_password(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "http_401"


def test_users_me_requires_valid_token(client: TestClient, admin_token: str) -> None:
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "admin"
    assert "X-Request-ID" in response.headers


def test_users_me_rejects_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer not-a-jwt"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "http_401"
