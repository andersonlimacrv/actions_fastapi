from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from enum import Enum


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: List[UserPublic]


class UserRoleEnum(str, Enum):
    admin = "ADMIN"
    user = "USER"
    hardware = "HARDWARE"


class UserDetail(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRoleEnum
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
