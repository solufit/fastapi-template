import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app import app
from database.models import User
from src.utils.database import Database
from src.scheme.user import UserCreate

client = TestClient(app)

db = Database()
db.connect()
session = db.SessionLocal()


@pytest.fixture(scope="module")
def test_db():
    db = Database(sqlite_path=":memory:")
    db.connect()
    yield db.SessionLocal()
    db.engine.dispose()


def test_create_user(test_db: Session) -> None:
    user_data = {"name": "John", "fullname": "John Doe", "nickname": "johnny"}
    response = client.post("/v1/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["fullname"] == user_data["fullname"]
    assert data["nickname"] == user_data["nickname"]


def test_get_user(test_db: Session) -> None:
    user_data = {"name": "Jane", "fullname": "Jane Doe", "nickname": "jane"}
    db_user = User(name=user_data["name"], fullname=user_data["fullname"], nickname=user_data["nickname"])
    test_db.add(db_user)
    test_db.commit()
    test_db.refresh(db_user)

    response = client.get(f"/v1/users/{db_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["fullname"] == user_data["fullname"]
    assert data["nickname"] == user_data["nickname"]


def test_delete_user(test_db: Session) -> None:
    user_data = {"name": "Jake", "fullname": "Jake Doe", "nickname": "jake"}
    db_user = User(name=user_data["name"], fullname=user_data["fullname"], nickname=user_data["nickname"])
    test_db.add(db_user)
    test_db.commit()
    test_db.refresh(db_user)

    response = client.delete(f"/v1/users/{db_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["fullname"] == user_data["fullname"]
    assert data["nickname"] == user_data["nickname"]

    response = client.get(f"/v1/users/{db_user.id}")
    assert response.status_code == 404
