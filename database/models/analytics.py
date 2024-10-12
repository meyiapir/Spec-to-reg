from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, str_pk

import datetime


class AnalyticsModel(Base):
    __tablename__ = "analytics"

    id: Mapped[str_pk]

    last_generation_time: Mapped[datetime.datetime | None]
    last_notification_time: Mapped[datetime.datetime | None]
    generations_count: Mapped[int] = mapped_column(default=0)

    coins_from_admins: Mapped[int] = mapped_column(default=0)
    coins_from_tasks: Mapped[int] = mapped_column(default=0)
    purchased_coins: Mapped[int] = mapped_column(default=0)
    referral_coins: Mapped[int] = mapped_column(default=0)

    likes_count: Mapped[int] = mapped_column(default=0)
    dislikes_count: Mapped[int] = mapped_column(default=0)
