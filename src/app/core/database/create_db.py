from src.app.core.database.db import engine, Base
import asyncio


async def create_db():
    async with engine.begin() as conn:
        from src.app.models.user import User

        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


asyncio.run(create_db())
