"""This module contains tests for the Database class."""

import pytest
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.utils.database import Database


def test_database_initialization_with_both_sqlite_and_mysql_params() -> None:
    """Test that Database initialization.

    raises ValueError when both sqlite_path and host db_name, db_user, db_pass are provided.
    """
    with pytest.raises(ValueError, match="You can't provide both sqlite_path and host, db_name, db_user, db_pass"):
        Database(sqlite_path="sqlite:///test.db", host="localhost", db_name="test_db", db_user="user", db_pass="pass")  # noqa: S106


def test_database_initialization_with_missing_mysql_params() -> None:
    """Test that Database initialization raises ValueError."""
    with pytest.raises(ValueError, match="You must provide host, db_name, db_user, db_pass"):
        Database(
            host="localhost",
            db_name="test_db",
            db_user="user",
            # Missing db_pass
        )


def test_database_initialization_with_missing_env_vars(monkeypatch: MonkeyPatch) -> None:
    """Test that Database initialization.

    Raises ValueError when MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER are missing.
    """
    monkeypatch.delenv("MYSQL_DATABASE", raising=False)
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)
    monkeypatch.delenv("MYSQL_USER", raising=False)
    with pytest.raises(ValueError, match="You must provide env variables MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER"):
        Database()


def test_database_connect_already_connected() -> None:
    """Test that Database.connect() does not re-create the engine if already connected."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    engine_first = db.engine
    db.connect()  # Should not re-create the engine
    engine_second = db.engine
    assert engine_first == engine_second


def test_database_session_commit() -> None:
    """Test that Database.session() commits the transaction."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    with db.session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_database_session_rollback() -> None:
    """Test that Database.session() rolls back the transaction on exception."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    with pytest.raises(SQLAlchemyError), db.session() as session:
        session.execute(text("INVALID SQL SYNTAX"))
    # Ensure session is cleaned up properly even after exception
    with db.session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1  # Should not raise an exception


def test_database_close_without_connection() -> None:
    """Test that Database.close() does not raise an exception when connection is not established."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.close()
    assert db.connection is False  # Should remain False


def test_database_double_close() -> None:
    """Test that Database.close() does not raise an exception when called twice."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    db.close()
    db.close()  # Closing again should not raise an exception
    assert db.connection is False


def test_database_del() -> None:
    """Test that Database.__del__() closes the connection without errors."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    del db  # Should call __del__ and close the connection without errors


def test_database_connect_failure_wrong_path() -> None:
    """Test that Database.connect() raises SQLAlchemyError when connection fails."""
    db = Database(sqlite_path="invalid_db_path")
    with pytest.raises(SQLAlchemyError, match="Error connecting to the database"):
        db.connect()


def test_database_engine_disposed_on_close() -> None:
    """Test that Database.engine is disposed on close."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    db.close()


def test_database_session_after_close() -> None:
    """Test that Database.session() raises ValueError after close."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    db.close()
    with pytest.raises(ValueError, match="Database connection is not established"), db.session():
        pass


def test_pytest_on_auto_set_db_path(monkeypatch: MonkeyPatch) -> None:
    """Test that Database.__init__() sets db_path to sqlite:///:memory: when pytest is enabled."""
    monkeypatch.delenv("PYTEST", raising=False)
    monkeypatch.delenv("PYTEST_DB", raising=False)

    monkeypatch.setenv("PYTEST", "true")
    db = Database()
    db.connect()
    assert db.db_path == "sqlite:///:memory:"


def test_dbpath_with_env(monkeypatch: MonkeyPatch) -> None:
    """Test that Database.__init__() sets db_path to mysql://user:pass@host/db_name when env variables are provided."""
    monkeypatch.delenv("PYTEST", raising=False)
    monkeypatch.delenv("PYTEST_DB", raising=False)

    monkeypatch.setenv("MYSQL_DATABASE", "test_db")
    monkeypatch.setenv("MYSQL_PASSWORD", "pass")
    monkeypatch.setenv("MYSQL_USER", "user")
    monkeypatch.setenv("MYSQL_HOST", "db")
    db = Database()
    assert db.db_path == "mysql://user:pass@db/test_db"


def test_dbpath_with_arg() -> None:
    """Test that Database.__init__() sets db_path to sqlite:///test.db when sqlite_path is provided."""
    db = Database(host="localhost", db_name="test_db", db_user="user", db_pass="pass")  # noqa: S106
    assert db.db_path == "mysql://user:pass@localhost/test_db"


def test_close_with_engine() -> None:
    """Test that Database.close() does not raise an exception when connection is not established."""
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    assert db.connection is True
    db.close()
    assert db.connection is False  # Should remain False


def test_close_without_engine(monkeypatch: MonkeyPatch) -> None:
    """Test that Database.close() does not raise an exception when connection is not established."""
    monkeypatch.setenv("PYTEST", "true")
    monkeypatch.delenv("PYTEST_DB", raising=False)

    db = Database()
    db.connect()
    db.close()
    assert db.connection is False  # Should remain False
    assert db.engine is None
