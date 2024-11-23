import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

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

    def __init__(self, sqlite_path: str | None = None) -> None:
        self.host = "db"
        self.sqlite_path = sqlite_path

        try:
            if os.environ["PYTEST"] == "true":
                self.sqlite_path = os.environ["PYTEST_DB"]
        except KeyError:
            pass

        try:
            self.database = os.environ["MYSQL_DATABASE"]
            self.user = os.environ["MYSQL_USER"]
            self.password = os.environ["MYSQL_PASSWORD"]
        except KeyError as e:
            try:
                _ = os.environ["PYTEST"] != "true"
            except KeyError:
                msg = f"Error reading environment variables: {e}"
                raise KeyError(msg) from None

        # Read PYTEST and PYTEST_DB environment variables
        pytest_env = os.getenv("PYTEST", "false").lower()
        pytest_db = os.getenv("PYTEST_DB")

        # Set sqlite_path to PYTEST_DB if PYTEST is true
        if pytest_env == "true" and pytest_db:
            self.sqlite_path = pytest_db

    def connect(self) -> None:
        """
        Connect to the database.
        This function generate
            - engine: The SQLAlchemy engine object for the database connection.
            - SessionLocal: The SQLAlchemy sessionmaker object for creating database sessions.
        """

        try:
            if self.sqlite_path is None:
                connection_string = f"mysql://{self.user}:{self.password}@{self.host}/{self.database}"
            else:
                connection_string = os.getenv("PYTEST_DB", "")
            self.engine = create_engine(connection_string)
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.SessionLocal.configure(expire_on_commit=False)

            try:
                if os.environ["PYTEST"] == "true":
                    Base.metadata.create_all(self.engine)

            except KeyError:
                pass

        except SQLAlchemyError as e:
            msg = f"Error connecting to the database: {e}"
            raise SQLAlchemyError(msg) from None

    def __del__(self) -> None:
        self._close()

    def _close(self) -> None:
        try:
            if self.engine:
                self.engine.dispose()
        except AttributeError:
            pass
