
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_address():
    response = client.post("/addresses", json={
        "name": "John",
        "street": "Main St",
        "city": "NYC",
        "latitude": 40.7128,
        "longitude": -74.0060
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John"

def test_get_addresses():
    response = client.get("/addresses")
    assert response.status_code == 200
