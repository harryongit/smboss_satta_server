from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_markets():
    resp = client.get("/api/markets")
    assert resp.status_code == 200


def test_offers():
    resp = client.get("/api/offers")
    assert resp.status_code == 200

