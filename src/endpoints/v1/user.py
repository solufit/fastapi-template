from fastapi import APIRouter, HTTPException

from database.models import User
from src.scheme.user import UserCreate, UserResponse
from src.utils.database import Database

router = APIRouter()


@router.post("/users")
def create_user(user: UserCreate) -> UserResponse:
    db = Database()
    db.connect()
    db_user = User(name=user.name, fullname=user.fullname, nickname=user.nickname)

    with db.session() as db_session:
        db_session.add(db_user)

    with db.session() as db_session:
        db_user_id = (
            db_session.query(User)
            .filter(User.name == user.name)
            .filter(User.fullname == user.fullname)
            .filter(User.nickname == user.nickname)
            .first()
        )

    if db_user_id is None:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user")

    return UserResponse(
        id=int(db_user_id.id), name=str(db_user.name), fullname=str(db_user.fullname), nickname=str(db_user.nickname)
    )


@router.get("/users/{user_id}")
def get_user(user_id: int) -> UserResponse:
    db = Database()
    db.connect()

    with db.session() as session:
        db_user = session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=int(db_user.id), name=str(db_user.name), fullname=str(db_user.fullname), nickname=str(db_user.nickname)
    )


@router.delete("/users/{user_id}")
def delete_user(user_id: int) -> UserResponse:
    db = Database()
    db.connect()

    with db.session() as session:
        db_user = session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return UserResponse(
        id=int(db_user.id), name=str(db_user.name), fullname=str(db_user.fullname), nickname=str(db_user.nickname)
    )
