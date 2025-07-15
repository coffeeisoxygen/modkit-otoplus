from fastapi.testclient import TestClient
from src.backend.app import app

client = TestClient(app)


def get_auth_token(username: str, password: str) -> str:
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]


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
    # Login untuk dapatkan token
    token = get_auth_token(user_payload["username"], user_payload["password"])
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f"Get failed: {response.text}"
    assert response.json()["id"] == user_id


def test_get_user_not_found(user_payload):
    # Login dulu agar dapat token
    user_payload["username"] = user_payload["username"].replace("_", "")
    client.post("/users/", json=user_payload)
    token = get_auth_token(user_payload["username"], user_payload["password"])
    response = client.get("/users/999999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404 or response.status_code == 422


def test_update_user_success(user_payload):
    user_payload["username"] = user_payload["username"].replace("_", "")
    # Ensure is_superuser is set to avoid IntegrityError
    user_payload.setdefault("is_superuser", False)
    create_resp = client.post("/users/", json=user_payload)
    assert create_resp.status_code in (200, 201)
    user_id = create_resp.json()["id"]
    token = get_auth_token(user_payload["username"], user_payload["password"])
    # Include is_superuser in update_data to avoid NOT NULL error
    update_data = {
        "email": "newemail@example.com",
        "is_superuser": user_payload["is_superuser"],
    }
    response = client.put(
        f"/users/{user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, f"Update failed: {response.text}"
    assert response.json()["email"] == "newemail@example.com"


def test_delete_user_success(user_payload):
    user_payload["username"] = user_payload["username"].replace("_", "")
    create_resp = client.post("/users/", json=user_payload)
    assert create_resp.status_code in (200, 201)
    user_id = create_resp.json()["id"]
    token = get_auth_token(user_payload["username"], user_payload["password"])
    response = client.delete(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f"Delete failed: {response.text}"
    assert response.json()["deleted"] is True
