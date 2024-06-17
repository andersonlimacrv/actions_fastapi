from src.app.core.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.app.models.regime import Regime


class Grupo(Base):
    __tablename__ = "grupos"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), unique=True)
    empresas = relationship(
        "Empresa",
        back_populates="grupo",
        cascade="all, delete",
    )
    is_active: Mapped[bool] = mapped_column(default=True)


class Empresa(Base):
    __tablename__ = "empresas"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), unique=True)
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id"))
    grupo = relationship("Grupo", back_populates="empresas")
    unidades = relationship("Unidade", back_populates="empresa", cascade="all, delete")
    is_active: Mapped[bool] = mapped_column(default=True)


class Unidade(Base):
    __tablename__ = "unidades"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), unique=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="unidades")
    regimes = relationship(
        "Regime",
        back_populates="unidade",
        cascade="all, delete",
    )
    is_active: Mapped[bool] = mapped_column(default=True)
