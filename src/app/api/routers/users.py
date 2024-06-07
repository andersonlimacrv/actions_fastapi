from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import get_current_user
from src.app.core.database.db import async_get_db_session
from src.app.models.user import User
from src.app.schemas.message import Message
from src.app.schemas.user import (
    UserSchema,
    UserPublic,
    UserList,
    UserDetail,
)
from src.app.services.users import UserService
from src.app.repositories.users import UserRepository

router = APIRouter(tags=["Users 💁🏻‍♂️"])

CurrentUser = Annotated[User, Depends(get_current_user)]
db_session = Annotated[AsyncSession, Depends(async_get_db_session)]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    summary="Create user",
)
async def create_user(user: UserSchema, db: db_session):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.create_user(user)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
    summary="Update user",
)
async def update_user(
    user_id: int, user: UserSchema, db: db_session, current_user: CurrentUser
):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.update_user(user_id, user, current_user)


@router.get(
    "", response_model=UserList, status_code=status.HTTP_200_OK, summary="Get all users"
)
async def read_users(db: db_session, current_user: CurrentUser):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return {"users": await user_service.get_all_users(current_user)}


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDetail,
    summary="Get user by id",
)
async def read_user(user_id: int, db: db_session, current_user: CurrentUser):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.get_user_by_id(user_id, current_user)


@router.delete(
    "/{user_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
    summary="Delete user",
)
async def delete_user(user_id: int, db: db_session, current_user: CurrentUser):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.delete_user(user_id, current_user)
