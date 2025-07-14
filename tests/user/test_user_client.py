from fastapi.testclient import TestClient
from src.backend.app import app

client = TestClient(app)


def test_create_user_success(user_payload):
    # Ensure username is alphanumeric (no underscores) to pass validation
    user_payload["username"] = user_payload["username"].replace("_", "")
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data["username"] == user_payload["username"]
    assert data["email"] == user_payload["email"]


def test_create_user_duplicate(user_payload):
    user_payload["username"] = user_payload["username"].replace("_", "")
    client.post("/users/", json=user_payload)  # First create
    response = client.post("/users/", json=user_payload)  # Duplicate
    assert response.status_code == 400 or response.status_code == 422


def test_get_user_success(user_payload):
    user_payload["username"] = user_payload["username"].replace("_", "")
    create_resp = client.post("/users/", json=user_payload)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    user_id = create_resp.json().get("id")
    assert user_id is not None, f"User ID missing in response: {create_resp.json()}"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, f"Get failed: {response.text}"
    assert response.json()["id"] == user_id


def test_get_user_not_found():
    response = client.get("/users/999999")
    assert response.status_code == 404 or response.status_code == 422
