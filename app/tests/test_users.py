from fastapi.testclient import TestClient


def test_list_users_paginated(client: TestClient) -> None:
    response = client.get("/api/v1/users?page=1&page_size=10")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "meta" in body
    assert body["meta"]["page"] == 1
    assert body["meta"]["page_size"] == 10
    assert isinstance(body["items"], list)


def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/api/v1/users",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "full_name": "New User",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["username"] == "newuser"
