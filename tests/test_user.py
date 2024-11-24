import random
import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from database.models import User
from src.app import app
from src.utils.database import Database

client = TestClient(app)


@pytest.fixture
def test_db() -> Generator[str, None, None]:
    path = f"sqlite:///{tempfile.gettempdir()}/{random.randint(1,1000)}test.db"
    yield path
    # path[0:10] is "sqlite:///", so we start from path[10:]
    Path(path[10:]).unlink()


def test_create_user(test_db: str) -> None:
    path = test_db
    with patch.dict("os.environ", {"PYTEST": "true", "PYTEST_DB": path}):
        user_data = {"name": "John", "fullname": "John Doe", "nickname": "johnny"}
        response = client.post("/v1/users", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["fullname"] == user_data["fullname"]
        assert data["nickname"] == user_data["nickname"]


def test_get_user(test_db: str) -> None:
    path = test_db
    with patch.dict("os.environ", {"PYTEST": "true", "PYTEST_DB": path}):
        user_data = {"name": "Jane", "fullname": "Jane Doe", "nickname": "jane"}
        db_user = User(name=user_data["name"], fullname=user_data["fullname"], nickname=user_data["nickname"])
        db = Database()
        db.connect()
        with db.session() as session:
            session.add(db_user)

        response = client.get(f"/v1/users/{db_user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["fullname"] == user_data["fullname"]
        assert data["nickname"] == user_data["nickname"]


def test_delete_user(test_db: str) -> None:
    path = test_db

    with patch.dict("os.environ", {"PYTEST": "true", "PYTEST_DB": path}):
        user_data = {"name": "Jake", "fullname": "Jake Doe", "nickname": "jake"}
        db_user = User(name=user_data["name"], fullname=user_data["fullname"], nickname=user_data["nickname"])

        db = Database()
        db.connect()

        with db.session() as session:
            session.add(db_user)

        response = client.delete(f"/v1/users/{db_user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["fullname"] == user_data["fullname"]
        assert data["nickname"] == user_data["nickname"]

        response = client.get(f"/v1/users/{db_user.id}")
        assert response.status_code == 404
