# Gunakan fixture user_payload dan admin_user_payload dari conftest.py


# tests/member/test_member_client.py
import uuid

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


def unique_member_payload() -> dict:
    uid = uuid.uuid4().hex[:8]
    return {
        "name": f"member{uid}",
        "ipaddress": f"192.168.1.{int(uid[:2], 16) % 255}",
        "urlreport": f"http://example.com/{uid}",
        "pin": "123456",
        "password": "StrongP@ss1",
        "is_active": True,
        "allow_no_sign": False,
    }


def ensure_admin_user():
    # Try to login, if fails, create the admin user
    resp = client.post(
        "/auth/login",
        data={"username": "Administrator", "password": "@Admin12345"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if resp.status_code == 200:
        return
    # Try to create admin user
    admin_payload = {
        "username": "Administrator",
        "email": "admin@example.com",
        "password": "@Admin12345",
        "is_admin": True,
        "is_active": True,
        "full_name": "Administrator",
    }
    # Try to create, ignore if already exists
    client.post("/users/", json=admin_payload)


def test_create_member_admin_success():
    ensure_admin_user()
    token = get_auth_token("Administrator", "@Admin12345")
    member_payload = unique_member_payload()
    response = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in (200, 201), f"Create failed: {response.text}"
    data = response.json()
    assert data["name"] == member_payload["name"]
    assert data["ipaddress"] == member_payload["ipaddress"]


def test_create_member_forbidden_for_non_admin(user_payload):
    resp = client.post("/users/", json=user_payload)
    assert resp.status_code in (200, 201), f"User create failed: {resp.text}"
    token = get_auth_token(user_payload["username"], user_payload["password"])
    member_payload = unique_member_payload()
    response = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in (403, 422)


def test_get_member_admin_success(user_payload):  # noqa: ARG001
    ensure_admin_user()
    token = get_auth_token("Administrator", "@Admin12345")
    member_payload = unique_member_payload()
    create_resp = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    member_id = create_resp.json()["id"]
    response = client.get(
        f"/v1/members/{member_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == member_id


def test_get_member_forbidden_for_non_admin(user_payload):
    # Buat admin
    admin_payload = user_payload.copy()
    admin_payload["username"] = admin_payload["username"].replace("testuser", "admin")
    admin_payload["email"] = admin_payload["email"].replace("testuser", "admin")
    resp = client.post("/users/", json=admin_payload)
    assert resp.status_code in (200, 201), f"User create failed: {resp.text}"
    admin_token = get_auth_token(admin_payload["username"], admin_payload["password"])
    member_payload = unique_member_payload()
    create_resp = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    if create_resp.status_code not in (200, 201):
        assert create_resp.status_code in (403, 422)
        return
    member_id = create_resp.json()["id"]
    # Buat user biasa
    user2_payload = user_payload.copy()
    user2_payload["username"] = user2_payload["username"] + "2"
    user2_payload["email"] = user2_payload["email"].replace("@", "2@")
    resp2 = client.post("/users/", json=user2_payload)
    assert resp2.status_code in (200, 201), f"User create failed: {resp2.text}"
    user_token = get_auth_token(user2_payload["username"], user2_payload["password"])
    response = client.get(
        f"/v1/members/{member_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code in (403, 422)


def test_update_member_admin_success(_user_payload):
    ensure_admin_user()
    token = get_auth_token("Administrator", "@Admin12345")
    member_payload = unique_member_payload()
    create_resp = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    member_id = create_resp.json()["id"]
    update_data = {"urlreport": "http://updated.com", "is_active": False}
    response = client.put(
        f"/v1/members/{member_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["urlreport"] == "http://updated.com"
    assert response.json()["is_active"] is False


def test_update_member_forbidden_for_non_admin(user_payload):
    # Buat admin
    admin_payload = user_payload.copy()
    admin_payload["username"] = admin_payload["username"].replace("testuser", "admin")
    admin_payload["email"] = admin_payload["email"].replace("testuser", "admin")
    resp = client.post("/users/", json=admin_payload)
    assert resp.status_code in (200, 201), f"User create failed: {resp.text}"
    admin_token = get_auth_token(admin_payload["username"], admin_payload["password"])
    member_payload = unique_member_payload()
    create_resp = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    if create_resp.status_code not in (200, 201):
        assert create_resp.status_code in (403, 422)
        return
    member_id = create_resp.json()["id"]
    # Buat user biasa
    user2_payload = user_payload.copy()
    user2_payload["username"] = user2_payload["username"] + "2"
    user2_payload["email"] = user2_payload["email"].replace("@", "2@")
    resp2 = client.post("/users/", json=user2_payload)
    assert resp2.status_code in (200, 201), f"User create failed: {resp2.text}"
    user_token = get_auth_token(user2_payload["username"], user2_payload["password"])
    update_data = {"urlreport": "http://forbidden.com"}
    response = client.put(
        f"/v1/members/{member_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code in (403, 422)


def test_delete_member_admin_success(_user_payload):
    ensure_admin_user()
    token = get_auth_token("Administrator", "@Admin12345")
    member_payload = unique_member_payload()
    create_resp = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    member_id = create_resp.json()["id"]
    response = client.delete(
        f"/v1/members/{member_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["deleted"] is True


def test_delete_member_forbidden_for_non_admin(user_payload):
    # Buat admin
    admin_payload = user_payload.copy()
    admin_payload["username"] = admin_payload["username"].replace("testuser", "admin")
    admin_payload["email"] = admin_payload["email"].replace("testuser", "admin")
    resp = client.post("/users/", json=admin_payload)
    assert resp.status_code in (200, 201), f"User create failed: {resp.text}"
    admin_token = get_auth_token(admin_payload["username"], admin_payload["password"])
    member_payload = unique_member_payload()
    create_resp = client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    if create_resp.status_code not in (200, 201):
        assert create_resp.status_code in (403, 422)
        return
    member_id = create_resp.json()["id"]
    # Buat user biasa
    user2_payload = user_payload.copy()
    user2_payload["username"] = user2_payload["username"] + "2"
    user2_payload["email"] = user2_payload["email"].replace("@", "2@")
    resp2 = client.post("/users/", json=user2_payload)
    assert resp2.status_code in (200, 201), f"User create failed: {resp2.text}"
    user_token = get_auth_token(user2_payload["username"], user2_payload["password"])
    response = client.delete(
        f"/v1/members/{member_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code in (403, 422)


def test_list_members_admin_success(_user_payload):
    ensure_admin_user()
    token = get_auth_token("Administrator", "@Admin12345")
    member_payload = unique_member_payload()
    client.post(
        "/v1/members/",
        json=member_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get("/v1/members/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(m["name"] == member_payload["name"] for m in response.json())


def test_list_members_forbidden_for_non_admin(user_payload):
    resp = client.post("/users/", json=user_payload)
    assert resp.status_code in (200, 201), f"User create failed: {resp.text}"
    token = get_auth_token(user_payload["username"], user_payload["password"])
    response = client.get("/v1/members/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (403, 422)
