from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    fullname: str
    nickname: str


class UserRetrieve(BaseModel):
    id: int
    name: str
    fullname: str
    nickname: str


class UserDelete(BaseModel):
    id: int
