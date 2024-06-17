from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import get_current_user
from src.app.core.database.db import async_get_db_session
from src.app.models.user import User
from src.app.schemas.message import Message
from src.app.schemas.group import GroupSchema, GroupList, GroupPublic
from src.app.services.group import GroupService
from src.app.repositories.group import GroupRepository


router = APIRouter(tags=["Grupos 💼"])

CurrentUser = Annotated[User, Depends(get_current_user)]
db_session = Annotated[AsyncSession, Depends(async_get_db_session)]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GroupPublic,
    summary="Create group",
)
async def create_group(group: GroupSchema, db: db_session):
    new_group = GroupService(GroupRepository(db))
    return await new_group.create_group(group)


@router.put(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=GroupPublic,
    summary="Update group",
)
async def update_group(group_id: int, group: GroupSchema, db: db_session):
    group_to_update = GroupService(GroupRepository(db))
    return await group_to_update.update_group(group_id, group)


@router.get(
    "",
    response_model=GroupList,
    status_code=status.HTTP_200_OK,
    summary="Get all groups",
)
async def read_groups(db: db_session):
    all_groups = GroupService(GroupRepository(db))
    return {"groups": await all_groups.get_all_groups()}


@router.get(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=GroupPublic,
    summary="Get group by id",
)
async def read_group(group_id: int, db: db_session):
    group_to_get = GroupService(GroupRepository(db))
    return await group_to_get.get_group_by_id(group_id)


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
    summary="Delete group",
)
async def delete_group(group_id: int, db: db_session):
    """W.I.P. NEED IMPLEMENTS -> WHEN DELE GROUP, DELETE ALL ASSOCIATED COMPANIES"""
    group_to_del = GroupService(GroupRepository(db))
    return await group_to_del.delete_group(group_id)
