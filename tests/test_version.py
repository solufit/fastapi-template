from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_version() -> None:
    response = client.get("/v1/")
    assert response.status_code == 200
    assert "version" in response.json()
    assert isinstance(response.json()["version"], str)
