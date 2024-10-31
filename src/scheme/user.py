from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    fullname: str
    nickname: str


class UserResponse(BaseModel):
    id: int
    name: str
    fullname: str
    nickname: str
