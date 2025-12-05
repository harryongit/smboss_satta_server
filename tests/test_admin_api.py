from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_admin_register_and_login():
    reg = client.post("/admin/auth/register", json={"username": "admin1", "email": "a@example.com", "password": "pass", "role": "admin"})
    assert reg.status_code == 200
    login = client.post("/admin/auth/login", json={"username": "admin1", "password": "pass"})
    assert login.status_code == 200
    assert "access_token" in login.json()

