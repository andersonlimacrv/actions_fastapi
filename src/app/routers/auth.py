from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus

from src.app.core.security import verify_password, create_access_token, get_current_user
from src.app.schemas.token import Token
from src.app.schemas.user import UserDB

from src.app.core.db.database import database
from src.app.core.utils import get_user_by_email


router = APIRouter(prefix="/auth", tags=["Auth 🔑"])


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh_token", response_model=Token)
def refresh_acess_token(user: UserDB = Depends(get_current_user)):
    new_access_token = create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}
