from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from typing import Annotated

from src.app.core.db.database import database
from src.app.schemas.message import Message
from src.app.core.security import (
    get_current_user,
    get_password_hash,
    protected_root_user,
)

from src.app.schemas.user import UserSchema, UserDB, UserPublic, UserList

router = APIRouter(prefix="/users", tags=["Users 💁🏻‍♂️"])
CurrentUser = Annotated[UserDB, Depends(get_current_user)]


def get_next_id() -> int:
    if not database:
        return 1
    return max(user.id for user in database) + 1


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    if any(u.username == user.username for u in database):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Username already exists"
        )

    hashed_password = get_password_hash(user.password)
    next_id = get_next_id()

    user_with_id = UserDB(
        id=next_id,
        hashed_password=hashed_password,
        **user.model_dump(),
    )
    database.append(user_with_id)

    return user_with_id


@router.get("/", response_model=UserList, status_code=HTTPStatus.OK)
def read_users(current_user: CurrentUser):
    return {"users": database}


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
@protected_root_user
def update_user(user_id: int, user: UserSchema, current_user: CurrentUser):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    hashed_password = get_password_hash(user.password)
    user_with_id = UserDB(
        id=user_id,
        hashed_password=hashed_password,
        **user.model_dump(),
    )

    return user_with_id


@router.delete("/{user_id}", response_model=Message)
@protected_root_user
def delete_user(user_id: int, current_user: CurrentUser):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    del database[user_id - 1]

    return {"message": "User deleted"}
