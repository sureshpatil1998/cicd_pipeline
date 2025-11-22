from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint returns greeting message."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Hello")


def test_health():
    """Test health check endpoint."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"