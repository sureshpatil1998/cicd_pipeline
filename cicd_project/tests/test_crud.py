import json
import pytest
from app import app, db, Item

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_and_get_item(client):
    resp = client.post("/items", json={"name": "chair", "description": "wooden"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "chair"
    item_id = data["id"]

    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["description"] == "wooden"

def test_list_items(client):
    client.post("/items", json={"name": "a", "description": "one"})
    client.post("/items", json={"name": "b", "description": "two"})
    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_update_item(client):
    resp = client.post("/items", json={"name": "x", "description": "old"})
    item_id = resp.get_json()["id"]
    resp = client.put(f"/items/{item_id}", json={"description": "new"})
    assert resp.status_code == 200
    assert resp.get_json()["description"] == "new"

def test_delete_item(client):
    resp = client.post("/items", json={"name": "to-delete", "description": ""})
    item_id = resp.get_json()["id"]
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 200
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404
