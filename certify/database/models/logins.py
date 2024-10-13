from __future__ import annotations

from sqlalchemy.orm import Mapped

from certify.database.models.base import Base, str_pk


class LoginsModel(Base):
    __tablename__ = "logins"

    username: Mapped[str_pk]
    name: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]
