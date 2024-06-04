from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated

from src.app.schemas.message import Message
from src.app.core.security import (
    get_current_user,
    get_password_hash,
)

from src.app.schemas.user import (
    UserSchema,
    UserPublic,
    UserList,
    UserDetail,
    UserRoleEnum,
)
from src.app.models.user import User
from src.app.core.database.db import async_get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

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
    stmt = await db.scalar(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )

    if stmt:
        if stmt.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        elif stmt.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")


@router.get(
    "", response_model=UserList, status_code=status.HTTP_200_OK, summary="Get all users"
)
async def read_users(db: db_session, current_user: CurrentUser):
    stmt = select(User)
    result = await db.scalars(stmt)
    users = result.all()
    return {"users": users}


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user(
    user_id: int, user: UserSchema, db: db_session, current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email

    try:
        await db.commit()
        await db.refresh(current_user)

        return current_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDetail,
    summary="Get user by id",
)
async def read_user(user_id: int, db: db_session, current_user: CurrentUser):
    if current_user.role == UserRoleEnum.admin or current_user.id == user_id:
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.scalars(stmt)
            user = result.first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            return user

        except Exception as e:
            if e.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with user_id {user_id} not found",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error getting user with user_id  {user_id}: {e}",
                )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )


@router.delete(
    "/{user_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
    summary="Delete user",
)
async def delete_user(user_id: int, db: db_session, current_user: CurrentUser):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    try:
        await db.delete(current_user)
        await db.commit()
        return {"message": f"User {user_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user{user_id}: {e}",
        )
