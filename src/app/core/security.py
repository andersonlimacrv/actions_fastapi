from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from http import HTTPStatus

from jwt import DecodeError, ExpiredSignatureError, decode, encode
from passlib.context import CryptContext

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from functools import wraps

from src.app.schemas.token import TokenData
from src.app.core.utils import get_user_by_email
from src.app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def protect_root(user_id: int):
    if user_id == 1:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Can't update this user"
        )


def protected_root_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get("user_id")
        if user_id == 1:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Can't update this user"
            )
        return func(*args, **kwargs)

    return wrapper


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = get_user_by_email(token_data.username)

    if user is None:
        raise credentials_exception

    return user
