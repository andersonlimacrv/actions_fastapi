from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import get_current_user
from src.app.core.database.db import async_get_db_session
from src.app.models.user import User
from src.app.schemas.message import Message
from src.app.schemas.company import CompanySchema, CompanyPublic, CompanyList
from src.app.services.company import CompanyService
from src.app.services.group import GroupService
from src.app.repositories.group import GroupRepository
from src.app.repositories.company import CompanyRepository


router = APIRouter(tags=["Empresas 🏭"])

CurrentUser = Annotated[User, Depends(get_current_user)]
db_session = Annotated[AsyncSession, Depends(async_get_db_session)]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CompanyPublic,
    summary="Create company",
)
async def create_company(company: CompanySchema, db: db_session):
    has_group = await GroupService(GroupRepository(db))._get_group_or_404(
        company.grupo_id
    )
    if has_group:
        new_company = CompanyService(CompanyRepository(db))

    return await new_company.create_company(company)


@router.put(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyPublic,
    summary="Update company",
)
async def update_company(company_id: int, company: CompanySchema, db: db_session):
    has_group = await GroupService(GroupRepository(db))._get_group_or_404(
        company.grupo_id
    )
    if has_group:
        company_to_update = CompanyService(CompanyRepository(db))
    return await company_to_update.update_company(company_id, company)


@router.get(
    "",
    response_model=CompanyList,
    status_code=status.HTTP_200_OK,
    summary="Get all companies",
)
async def read_companies(db: db_session):
    all_companies = CompanyService(CompanyRepository(db))
    return {"empresas": await all_companies.get_all_companies()}


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyPublic,
    summary="Get company by id",
)
async def read_company(company_id: int, db: db_session):
    company_to_get = CompanyService(CompanyRepository(db))
    return await company_to_get.get_company_by_id(company_id)


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
    summary="Delete company",
)
async def delete_company(company_id: int, db: db_session):
    company_to_delete = CompanyService(CompanyRepository(db))
    return await company_to_delete.delete_company(company_id)
