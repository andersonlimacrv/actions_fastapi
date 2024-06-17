from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.app.models.organization import Grupo


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_group_by_id(self, group_id: int) -> Grupo:
        stmt = await self.session.get(Grupo, group_id)
        return stmt

    async def get_group_by_name(self, group_name: str) -> Grupo:
        stmt = select(Grupo).where(Grupo.nome == group_name)
        result = await self.session.scalars(stmt)
        return result.first()

    async def add_group(self, group: Grupo) -> Grupo:
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def update_group(self, grupo_id: int, group_data: dict) -> Grupo:
        stmt = select(Grupo).where(Grupo.id == grupo_id)
        result = await self.session.scalars(stmt)
        existing_group = result.one_or_none()

        if not existing_group:
            return None

        existing_group.nome = group_data.nome
        try:
            self.session.add(existing_group)
            await self.session.commit()
            await self.session.refresh(existing_group)
            return existing_group
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_all_groups_repository(self) -> list[Grupo]:
        stmt = select(Grupo)
        result = await self.session.scalars(stmt)
        return result.all()

    async def delete_group(self, group_id: int):
        stmt = delete(Grupo).where(Grupo.id == group_id)
        await self.session.execute(stmt)
        await self.session.commit()
