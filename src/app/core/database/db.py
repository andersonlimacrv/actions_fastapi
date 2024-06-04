from sqlalchemy import event
from sqlalchemy.engine import Engine
from src.app.core.config import settings
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker, MappedAsDataclass
from typing import AsyncGenerator


class Base(MappedAsDataclass, DeclarativeBase): ...


db_url = make_url(settings.DATABASE_ACTIONS_URL)
async_engine = create_async_engine(db_url, echo=True, echo_pool=False)
local_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)


async def async_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = local_session
    async with async_session() as db_session:
        yield db_session
