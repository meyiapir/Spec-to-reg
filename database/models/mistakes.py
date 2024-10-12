from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base, created_at, str_pk


class MistakesModel(Base):
    __tablename__ = "mistakes"

    id: Mapped[str_pk] = mapped_column(index=True)
    created_at: Mapped[created_at]
    reason: Mapped[str]
