from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database.models import User
from src.scheme.user import UserCreate, UserResponse
from src.utils.database import Database

router = APIRouter()

db = Database()
db.connect()
session = db.SessionLocal()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends()) -> UserResponse:
    db = session
    db_user = User(name=user.name, fullname=user.fullname, nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(id=db_user.id, name=db_user.name, fullname=db_user.fullname, nickname=db_user.nickname)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends()) -> UserResponse:
    db = session
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=db_user.id, name=db_user.name, fullname=db_user.fullname, nickname=db_user.nickname)


@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends()) -> UserResponse:
    db = session
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return UserResponse(id=db_user.id, name=db_user.name, fullname=db_user.fullname, nickname=db_user.nickname)
