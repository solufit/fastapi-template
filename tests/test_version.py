from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_version() -> None:
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}
