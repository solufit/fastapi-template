import pytest
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.utils.database import Database


def test_database_initialization_with_both_sqlite_and_mysql_params() -> None:
    """
    Test that Database initialization raises ValueError
    when both sqlite_path and host, db_name, db_user, db_pass are provided.
    """
    with pytest.raises(ValueError, match="You can't provide both sqlite_path and host, db_name, db_user, db_pass"):
        Database(sqlite_path="sqlite:///test.db", host="localhost", db_name="test_db", db_user="user", db_pass="pass")  # noqa: S106


def test_database_initialization_with_missing_mysql_params() -> None:
    """
    Test that Database initialization raises ValueError
    """
    with pytest.raises(ValueError, match="You must provide host, db_name, db_user, db_pass"):
        Database(
            host="localhost",
            db_name="test_db",
            db_user="user",
            # Missing db_pass
        )


def test_database_initialization_with_missing_env_vars(monkeypatch: MonkeyPatch) -> None:
    """
    Test that Database initialization raises ValueError when MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER are missing.
    """
    monkeypatch.delenv("MYSQL_DATABASE", raising=False)
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)
    monkeypatch.delenv("MYSQL_USER", raising=False)
    with pytest.raises(ValueError, match="You must provide env variables MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER"):
        Database()


def test_database_connect_already_connected() -> None:
    """
    Test that Database.connect() does not re-create the engine if already connected.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    engine_first = db.engine
    db.connect()  # Should not re-create the engine
    engine_second = db.engine
    assert engine_first == engine_second


def test_database_session_commit() -> None:
    """
    Test that Database.session() commits the transaction.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    with db.session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_database_session_rollback() -> None:
    """
    Test that Database.session() rolls back the transaction on exception.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    with pytest.raises(SQLAlchemyError), db.session() as session:
        session.execute(text("INVALID SQL SYNTAX"))
    # Ensure session is cleaned up properly even after exception
    with db.session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1  # Should not raise an exception


def test_database_close_without_connection() -> None:
    """
    Test that Database.close() does not raise an exception when connection is not established.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.close()
    assert db.connection is False  # Should remain False


def test_database_double_close() -> None:
    """
    Test that Database.close() does not raise an exception when called twice.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    db.close()
    db.close()  # Closing again should not raise an exception
    assert db.connection is False


def test_database_del() -> None:
    """
    Test that Database.__del__() closes the connection without errors.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    del db  # Should call __del__ and close the connection without errors


def test_database_connect_failure_wrong_path() -> None:
    """
    Test that Database.connect() raises SQLAlchemyError when connection fails.
    """
    db = Database(sqlite_path="invalid_db_path")
    with pytest.raises(SQLAlchemyError, match="Error connecting to the database"):
        db.connect()


def test_database_engine_disposed_on_close() -> None:
    """
    Test that Database.engine is disposed on close.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    db.close()


def test_database_session_after_close() -> None:
    """
    Test that Database.session() raises ValueError after close.
    """
    db = Database(sqlite_path="sqlite:///:memory:")
    db.connect()
    db.close()
    with pytest.raises(ValueError, match="Database connection is not established"), db.session():
        pass
