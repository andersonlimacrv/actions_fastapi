from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy import or_
from src.app.models.user import User


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


async def get_user_bt_username(self, username: str) -> User:
    stmt = await self.session.scalar(User.username == username)
    return stmt
