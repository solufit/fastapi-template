import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.app_detail import APIDetail


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_get_version(client: TestClient) -> None:
    response = client.get("/v1/")
    assert response.status_code == 200
    assert "version" in response.json()
    assert isinstance(response.json()["version"], str)
    assert response.json()["version"] == APIDetail.VERSION
