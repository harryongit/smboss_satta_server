from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_markets():
    resp = client.get("/public/markets")
    assert resp.status_code == 200


def test_offers():
    resp = client.get("/public/offers")
    assert resp.status_code == 200

