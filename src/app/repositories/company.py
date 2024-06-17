from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.app.models.organization import Empresa


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_company_by_id(self, company_id: int) -> Empresa:
        stmt = await self.session.get(Empresa, company_id)
        return stmt

    async def get_company_by_name(self, company_name: str) -> Empresa:
        stmt = select(Empresa).where(Empresa.nome == company_name)
        result = await self.session.scalars(stmt)
        return result.first()

    async def add_company(self, company: Empresa) -> Empresa:
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def update_company(self, company_id: int, company_data: dict) -> Empresa:
        stmt = select(Empresa).where(Empresa.id == company_id)
        result = await self.session.scalars(stmt)
        existing_company = result.one_or_none()

        if not existing_company:
            return None

        existing_company.nome = company_data.nome
        try:
            self.session.add(existing_company)
            await self.session.commit()
            await self.session.refresh(existing_company)
            return existing_company
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_all_companies_repository(self) -> list[Empresa]:
        stmt = select(Empresa)
        result = await self.session.scalars(stmt)
        return result.all()

    async def delete_company(self, company_id: int):
        stmt = delete(Empresa).where(Empresa.id == company_id)
        await self.session.execute(stmt)
        await self.session.commit()
