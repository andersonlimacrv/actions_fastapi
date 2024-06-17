from pydantic import BaseModel, ConfigDict
from typing import List


class CompanySchema(BaseModel):
    nome: str
    grupo_id: int


class CompanyPublic(BaseModel):
    id: int
    nome: str
    grupo_id: int
    model_config = ConfigDict(from_attributes=True)


class CompanyList(BaseModel):
    empresas: List[CompanyPublic]
