from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jwt import DecodeError, ExpiredSignatureError, decode, encode
from passlib.context import CryptContext

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from src.app.core.database.db import async_get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User
from sqlalchemy import select

from src.app.schemas.token import TokenData
from src.app.core.config import settings
from typing import Annotated


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
Token = Annotated[str, Depends(oauth2_scheme)]
db_session = Annotated[AsyncSession, Depends(async_get_db_session)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "name": ""})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY_HASH, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "name": ""})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY_HASH_REFRESH, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def check_refresh_token(token: Token, db: db_session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY_HASH_REFRESH, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = await db.scalar(select(User).where(User.username == token_data.username))

    if user is None:
        raise credentials_exception

    return user


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: Token, db: db_session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY_HASH, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
        token_data = TokenData(username=user_id)

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = await db.scalar(select(User).where(User.username == token_data.username))

    if user is None:
        raise credentials_exception

    return user
