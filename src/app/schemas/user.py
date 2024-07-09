from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from enum import Enum
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserAllow(BaseModel):
    is_active: bool
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserRoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    hardware = "hardware"


class UserDetail(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRoleEnum
    is_active: bool
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: List[UserDetail]
