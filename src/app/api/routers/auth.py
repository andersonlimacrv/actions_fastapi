from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.core.database.db import async_get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from src.app.core.security import verify_password, create_access_token, get_current_user
from src.app.schemas.token import Token
from src.app.models.user import User

router = APIRouter(tags=["Auth 🔑"])

db_session = Annotated[AsyncSession, Depends(async_get_db_session)]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
current_user = Annotated[User, Depends(get_current_user)]


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: FormData, db: db_session):

    stm = select(User).where(User.username == form_data.username)
    user = await db.scalar(stm)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh_token", response_model=Token)
async def refresh_acess_token(user: current_user):
    new_access_token = create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "Bearer"}
