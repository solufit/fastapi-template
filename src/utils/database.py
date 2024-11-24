from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from database.models import Base


class Database:
    """
    A class representing a database connection.

    Attributes:
        host (str): The hostname of the database server.
        database (str): The name of the database.
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        engine: The SQLAlchemy engine object for the database connection.
        SessionLocal: The SQLAlchemy sessionmaker object for creating database sessions.
    """

    db_path = ""
    connection = False

    def __init__(
        self,
        sqlite_path: str | None = None,
        host: str | None = None,
        db_name: str | None = None,
        db_user: str | None = None,
        db_pass: str | None = None,
    ) -> None:
        self.pytest_enabled = os.getenv("PYTEST", "false").lower() == "true"
        pytest_path = os.getenv("PYTEST_DB", "")

        # if pytest is enabled, set the db path to the pytest_path
        # if not provied pytest_path, set it to in-memory sqlite
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

            if db_name and db_pass and db_user:
                self.db_path = f"mysql://{db_user}:{db_pass}@db/{db_name}"
            else:
                msg = "You must provide env variables MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER"
                raise ValueError(msg)

    def connect(self) -> Database:
        """
        Connect to the database.
        This function generate
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

        return self

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Create a new session for the database connection.
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

        session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = session_local()

        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            msg = f"Error in session: {e}"
            raise SQLAlchemyError(msg) from None
        finally:
            session.close()

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        try:
            if self.engine:
                self.engine.dispose()
        except AttributeError:
            pass
        finally:
            self.connection = False
