from fastapi import APIRouter
from .routers import group, root, users, auth, company

api_router = APIRouter()

api_router.include_router(root.router, prefix="")
api_router.include_router(users.router, prefix="/users")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(group.router, prefix="/group")
api_router.include_router(company.router, prefix="/company")
