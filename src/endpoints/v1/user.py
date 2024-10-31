from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import User
from src.scheme.user import UserCreate, UserResponse
from src.utils.database import Database

router = APIRouter()


# データベースセッションを取得する依存関係


def get_db() -> Generator[Session, None, None]:
    db = Database()
    db.connect()
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate) -> UserResponse:
    db = Depends(get_db)
    db_user = User(name=user.name, fullname=user.fullname, nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
        id=int(db_user.id), name=str(db_user.name), fullname=str(db_user.fullname), nickname=str(db_user.nickname)
    )


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    db = Depends(get_db)
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=int(db_user.id), name=str(db_user.name), fullname=str(db_user.fullname), nickname=str(db_user.nickname)
    )


@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int) -> UserResponse:
    db = Depends(get_db)
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return UserResponse(
        id=int(db_user.id), name=str(db_user.name), fullname=str(db_user.fullname), nickname=str(db_user.nickname)
    )
