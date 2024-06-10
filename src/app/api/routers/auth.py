from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.core.database.db import async_get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from src.app.schemas.token import Token, RefreshToken, RefreshTokenData
from src.app.models.user import User
from src.app.repositories.users import UserRepository

router = APIRouter(tags=["Auth 🔑"])

db_session = Annotated[AsyncSession, Depends(async_get_db_session)]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
current_user = Annotated[User, Depends(get_current_user)]
refreshToken = Annotated[RefreshTokenData, Depends()]


@router.post("/login", response_model=RefreshToken)
async def login_for_access_token(form_data: FormData, db: db_session):
    user = await UserRepository(db).get_user_by_username(username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.id})
    response = RefreshToken(
        access_token=access_token, token_type="Bearer", refresh_token=refresh_token
    )

    return response


@router.post("/refresh_token", response_model=RefreshToken)
async def refresh_acess_token(refresh_token_data: refreshToken, user: current_user):
    """WIP - está aceitando qualquer refresh token, futuramente irá ser salvo para comparar."""
    new_access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.id})

    response = RefreshToken(
        access_token=new_access_token,
        token_type="Bearer",
        refresh_token=new_refresh_token,
    )

    return response
