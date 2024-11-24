from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """

    name: str
    fullname: str
    nickname: str


class UserResponse(BaseModel):
    """
    Represents the response model for a user.
    """

    id: int
    name: str
    fullname: str
    nickname: str
