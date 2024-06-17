from pydantic import BaseModel


class UnidadeSchema(BaseModel):
    id: int
    nome: str
    empresa_id: int
