import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.db.database import database
from src.app.routers import auth, root, users
from src.app.schemas.user import UserDB
from src.app.core.security import get_password_hash
from src.app.core.config import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(root.router)


def create_root_user():
    user = UserDB(
        id=settings.ROOT_ID,
        username=settings.ROOT_USERNAME,
        email=settings.ROOT_EMAIL,
        hashed_password=get_password_hash(settings.ROOT_PASSWORD),
        password=settings.ROOT_PASSWORD,
    )
    database.append(user)


create_root_user()


def start():
    """Launched with 'poetry run start' at root level."""
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8888, reload=True)
