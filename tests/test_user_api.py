from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_user_register_and_login():
    reg = client.post("/user/auth/register", json={"username": "user1", "email": "u@example.com", "password": "pass"})
    assert reg.status_code == 200
    login = client.post("/user/auth/login", json={"username": "user1", "password": "pass"})
    assert login.status_code == 200
    assert "access_token" in login.json()

