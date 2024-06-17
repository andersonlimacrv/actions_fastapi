from pydantic import BaseModel, ConfigDict
from typing import List


class GroupSchema(BaseModel):
    nome: str


class GroupPublic(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class GroupList(BaseModel):
    groups: List[GroupPublic]
