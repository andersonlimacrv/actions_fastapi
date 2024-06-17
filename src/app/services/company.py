from fastapi import HTTPException
from src.app.schemas.message import Message
from src.app.repositories.company import CompanyRepository
from src.app.schemas.company import CompanySchema
from src.app.models.organization import Empresa
from src.app.services.group import GroupService


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    async def create_company(self, company_data: CompanySchema) -> Empresa:
        new_company = Empresa(
            nome=company_data.nome,
            grupo_id=company_data.grupo_id,
        )

        if await self.company_repository.get_company_by_name(company_data.nome):
            raise HTTPException(status_code=400, detail="Company already exists")

        try:
            return await self.company_repository.add_company(new_company)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error creating company : " + str(e)
            )

    async def _get_company_or_404(self, company_id: int) -> Empresa:
        company = await self.company_repository.get_company_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=404, detail=f"Company with id: {company_id} not found"
            )
        return company

    async def update_company(self, company_id: int, company_data: dict) -> Empresa:
        updated_company = await self.company_repository.update_company(
            company_id, company_data
        )
        if not updated_company:
            raise HTTPException(
                status_code=404, detail=f"Company with id: {company_id} not found"
            )
        return updated_company

    async def get_all_companies(self) -> list[Empresa]:
        try:
            return await self.company_repository.get_all_companies_repository()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving companies: {e}"
            )

    async def get_company_by_id(self, company_id: int) -> Empresa:
        return await self._get_company_or_404(company_id)

    async def delete_company(self, company_id: int) -> Message:
        await self._get_company_or_404(company_id)
        try:
            await self.company_repository.delete_company(company_id)
            return Message(
                message=f"Company with id: {company_id} deleted successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting company: {e}")
