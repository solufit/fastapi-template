import os
from typing import Any

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

# ---------------------------------------------------------------
# SQLの初期設定

USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE = os.getenv("MYSQL_DATABASE")

path = f"mysql://{USER}:{PASSWORD}@db/{DATABASE}"
# path = 'mysql+pymysql://root:@127.0.0.1:3306/alembic_sample'

if path is not None:
    # Engine の作成
    Engine = create_engine(path, echo=False)
else:
    msg = "DATABASE_URL environment variable is not set."
    raise ValueError(msg)

Base: Any = declarative_base()

# ---------------------------------------------------------------


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    fullname = Column(String(255))
    nickname = Column(String(255))

    def __repr__(self) -> str:
        return f"<User('name={self.name}', fullname={self.fullname}, nickname={self.nickname})>"
