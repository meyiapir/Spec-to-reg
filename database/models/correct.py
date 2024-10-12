from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base, created_at, str_pk


class CorrectModel(Base):
    __tablename__ = "correct"

    id: Mapped[str_pk] = mapped_column(index=True)
    created_at: Mapped[created_at]
    comment: Mapped[str]
