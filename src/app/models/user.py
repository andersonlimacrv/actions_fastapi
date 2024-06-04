from datetime import datetime

from sqlalchemy import func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.database.db import Base
from src.app.schemas.user import UserRoleEnum


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=False)
    update_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
        default=None,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=None
    )
    is_active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.user
    )
