"""This module contains tests for the version endpoint of the FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.app_detail import APIDetail


@pytest.fixture
def client() -> TestClient:
    """Fixture that provides a test client for the FastAPI application."""
    return TestClient(app)


def test_get_version(client: TestClient) -> None:
    """Test the version endpoint of the FastAPI application."""
    response = client.get("/v1/")
    assert response.status_code == 200
    assert "version" in response.json()
    assert isinstance(response.json()["version"], str)
    assert response.json()["version"] == APIDetail.VERSION
