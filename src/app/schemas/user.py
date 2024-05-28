from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(UserSchema):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    create_at: datetime = datetime.now()


class UserList(BaseModel):
    users: list[UserPublic]
