from fastapi import APIRouter
from .routers import root, users, auth

api_router = APIRouter()

api_router.include_router(root.router, prefix="")
api_router.include_router(users.router, prefix="/users")
api_router.include_router(auth.router, prefix="/auth")
