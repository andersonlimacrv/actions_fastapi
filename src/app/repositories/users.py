from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy import or_
from src.app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = await self.session.get(User, user_id)
        return stmt

    async def get_user_by_username_or_email(self, username: str, email: str) -> User:
        stmt = await self.session.scalar(
            select(User).where(or_(User.username == username, User.email == email))
        )
        return stmt

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all_users_repository(self) -> list[User]:
        stmt = select(User)
        result = await self.session.scalars(stmt)
        return result.all()

    async def delete_user(self, user_id: int):
        stmt = delete(User).where(User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
