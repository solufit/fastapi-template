"""This module provides the Database class for managing database connections and sessions."""

from __future__ import annotations

import os
from contextlib import contextmanager, suppress
from typing import TYPE_CHECKING

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.exc import DetachedInstanceError

from database.models import Base

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Generator


class Database:
    """The `Database` class provides an interface for connecting to and interacting with a database.

    It supports both SQLite and MySQL databases, allowing for flexible configuration through
    direct parameters or environment variables. The class also supports a testing mode using pytest,
    enabling the use of an in-memory SQLite database.

    Attributes:
        db_path (str): The database connection string.
        connection (bool): Indicates whether a connection to the database has been established.
        pytest_enabled (bool): Indicates whether pytest is enabled. If env PYTEST is set to true, this will be True.

    Methods:
        connect() -> Database:
            Establishes a connection to the database.

        session() -> Generator[Session, None, None]:
            Provides a context manager for database sessions.

        close() -> None:
            Closes the database connection.
    """

    db_path = ""
    connection = False
    endgine: Engine | None = None

    def __init__(
        self,
        sqlite_path: str | None = None,
        host: str | None = None,
        db_name: str | None = None,
        db_user: str | None = None,
        db_pass: str | None = None,
    ) -> None:
        """Initialize the Database class.

        If env PYTEST is set to true, it will use the env PYTEST_DB as the database path
        and, sqlite_path, host, db_name, db_user, db_pass will be ignored.

        And,if sqlite_path, host, db_name, db_user, db_pass is not provided,
        it will read the values from the environment variables
        - MYSQL_DATABASE
        - MYSQL_PASSWORD
        - MYSQL_USER.

        Args:
            sqlite_path (str | None): The path to the SQLite database.
            host (str | None): The hostname of the database server.
            db_name (str | None): The name of the database.
            db_user (str | None): The username for the database connection.
            db_pass (str | None): The password for the database connection.
        """
        self.pytest_enabled = os.getenv("PYTEST", "false").lower() == "true"
        pytest_path = os.getenv("PYTEST_DB", "")

        # if pytest is enabled, set the db path to the pytest_path
        # if not provided pytest_path, set it to in-memory sqlite
        if self.pytest_enabled:
            if not pytest_path:
                pytest_path = "sqlite:///:memory:"
            self.db_path = pytest_path

        # you can't provide both sqlite_path and host, db_name, db_user, db_pass
        elif sqlite_path and (host or db_name or db_user or db_pass):
            msg = "You can't provide both sqlite_path and host, db_name, db_user, db_pass"
            raise ValueError(msg)

        # if sqlite_path provided, set the db_path to sqlite_path
        elif sqlite_path:
            self.db_path = sqlite_path

        # if host, db_name, db_user, db_pass provided, set the db_path to mysql
        elif host or db_name or db_user or db_pass:
            # check all the required fields are provided
            if not all([host, db_name, db_user, db_pass]):
                msg = "You must provide host, db_name, db_user, db_pass"
                raise ValueError(msg)

            self.db_path = f"mysql://{db_user}:{db_pass}@{host}/{db_name}"

        # if nothing provided, read value from env
        else:
            db_name = os.getenv("MYSQL_DATABASE", "")
            db_pass = os.getenv("MYSQL_PASSWORD", "")
            db_user = os.getenv("MYSQL_USER", "")
            db_host = os.getenv("MYSQL_HOST", "db")

            if db_name and db_pass and db_user:
                self.db_path = f"mysql://{db_user}:{db_pass}@{db_host}/{db_name}"
            else:
                msg = "You must provide env variables MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER"
                raise ValueError(msg)

    def connect(self) -> Database:
        """Connect to the database.

        This function generates
            - engine: The SQLAlchemy engine object for the database connection.

        return: Database object
        """
        if self.connection:
            return self

        try:
            self.engine = create_engine(self.db_path)

            # create all tables if pytest is enabled
            if self.pytest_enabled:
                Base.metadata.create_all(self.engine)

        except SQLAlchemyError as e:
            msg = f"Error connecting to the database: {e}"
            raise SQLAlchemyError(msg) from None

        self.connection = True

        return self

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Create a new session for the database connection.

        This function generate
            - session: The SQLAlchemy session object for the database connection.

        Example:
        ```python
        db = Database().connect()
        with db.session() as session:
            session.query(User).all()
        ```
        """
        if self.connection is False:
            msg = "Database connection is not established"
            raise ValueError(msg)

        session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        session = session_local()

        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            msg = f"Error in session: {e}"
            raise SQLAlchemyError(msg) from None
        finally:
            with suppress(DetachedInstanceError):
                session.close()

    def __del__(self) -> None:
        """Close the database connection when the object is deleted."""
        self.close()

    def close(self) -> None:
        """Close the database connection.

        This method disposes of the SQLAlchemy engine, effectively closing the connection to the database.
        It also sets the `connection` attribute to `False` to indicate that the connection is no longer active.
        """
        try:
            if self.engine:
                self.engine.dispose()
        except AttributeError:
            pass
        finally:
            self.endgine = None
            self.connection = False
