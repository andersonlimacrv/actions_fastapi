from src.app.core.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Regime(Base):
    __tablename__ = "regimes"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), unique=True)
    unidade_id = mapped_column(ForeignKey("unidades.id"))
    unidade: Mapped["Unidade"] = relationship(back_populates="regimes")
    is_active: Mapped[bool] = mapped_column(default=True)
