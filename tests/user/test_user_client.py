import pytest
from fastapi.testclient import TestClient
from src.backend.app import app

client = TestClient(app)


@pytest.fixture
def user_payload():
    return {
        "username": "testuser",
        "password": "@Secret123",
        "password_confirm": "@Secret123",
        "email": "testuser@example.com",
    }


def test_create_user_success(user_payload):
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data["username"] == user_payload["username"]
    assert data["email"] == user_payload["email"]

def test_create_user_duplicate(user_payload):
    client.post("/users/", json=user_payload)  # First create
    response = client.post("/users/", json=user_payload)  # Duplicate
    assert response.status_code == 400 or response.status_code == 422


def test_get_user_success(user_payload):
    create_resp = client.post("/users/", json=user_payload)
    user_id = create_resp.json().get("id")
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_not_found():
    response = client.get("/users/999999")
    assert response.status_code == 404 or response.status_code == 422
