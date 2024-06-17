from fastapi import HTTPException
from src.app.schemas.message import Message
from src.app.repositories.group import GroupRepository
from src.app.schemas.group import GroupSchema, GroupList
from src.app.models.organization import Grupo


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    async def create_group(self, group_data: GroupSchema) -> Grupo:
        new_group = Grupo(nome=group_data.nome)

        if await self.group_repository.get_group_by_name(group_data.nome):
            raise HTTPException(status_code=400, detail="Group already exists")

        try:
            return await self.group_repository.add_group(new_group)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error creating group : " + str(e)
            )

    async def _get_group_or_404(self, group_id: int) -> Grupo:
        group = await self.group_repository.get_group_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=404, detail=f"Group with id: {group_id} not found"
            )
        return group

    async def update_group(self, group_id: int, group_data: dict) -> Grupo:
        updated_group = await self.group_repository.update_group(group_id, group_data)
        if not updated_group:
            raise HTTPException(
                status_code=404, detail=f"Group with id: {group_id} not found"
            )
        return updated_group

    async def get_all_groups(self) -> list[Grupo]:
        try:
            return await self.group_repository.get_all_groups_repository()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving groups: {e}")

    async def get_group_by_id(self, group_id: int) -> Grupo:
        return await self._get_group_or_404(group_id)

    async def delete_group(self, group_id: int) -> Message:
        await self._get_group_or_404(group_id)
        try:
            await self.group_repository.delete_group(group_id)
            return Message(message=f"Group with id: {group_id} deleted successfully")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting group: {e}")
