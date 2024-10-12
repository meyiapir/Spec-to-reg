from __future__ import annotations
from datetime import datetime

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, created_at, str_pk


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str_pk] = mapped_column(index=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    language_code: Mapped[str | None]
    referrer: Mapped[str | None]
    created_at: Mapped[created_at]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    styles: Mapped[JSON] = mapped_column(JSON)
    quota: Mapped[int] = mapped_column(default=0)
    daily_quota: Mapped[int] = mapped_column(default=20)

    is_main_channel_sub: Mapped[bool] = mapped_column(default=False, nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_bro: Mapped[bool] = mapped_column(default=False)
    is_noder: Mapped[bool] = mapped_column(default=False)
    is_block: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)
    is_left: Mapped[datetime | None] = mapped_column(nullable=True)
