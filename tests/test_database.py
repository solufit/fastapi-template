import os
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.utils.database import Database


def test_database_init_success() -> None:
    """Test successful initialization of the Database class."""
    with patch.dict(
        os.environ, {"MYSQL_DATABASE": "test_db", "MYSQL_USER": "test_user", "MYSQL_PASSWORD": "test_password"}
    ):
        db = Database()
        assert db.host == "db"
        assert db.database == "test_db"
        assert db.user == "test_user"
        assert db.password == "test_password"  # noqa: S105


def test_database_init_missing_env_vars() -> None:
    """Test initialization of the Database class when environment variables are missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(KeyError) as excinfo:
            Database()
        assert "Error reading environment variables" in str(excinfo.value)


def test_database_init_connection_error() -> None:
    """Test initialization of the Database class when there is an error connecting to the database."""
    with (
        patch.dict(
            os.environ, {"MYSQL_DATABASE": "test_db", "MYSQL_USER": "test_user", "MYSQL_PASSWORD": "test_password"}
        ),
        patch("src.utils.database.create_engine", side_effect=SQLAlchemyError("Connection error")),
    ):
        db = Database(sqlite_path=":memory")

        with pytest.raises(SQLAlchemyError) as excinfo:
            db.connect()

        assert "Error connecting to the database" in str(excinfo.value)
