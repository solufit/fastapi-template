from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database.models import User
from src.scheme.user import UserCreate, UserRetrieve, UserDelete
from src.utils.database import Database

router = APIRouter()

db = Database()
db.connect()
SessionLocal = db.SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/user", response_model=UserRetrieve)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserRetrieve:
    db_user = User(name=user.name, fullname=user.fullname, nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/user/{user_id}", response_model=UserRetrieve)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRetrieve:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/user/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserDelete:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"id": user_id}
