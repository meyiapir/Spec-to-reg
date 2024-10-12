from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, created_at, universal_id

import datetime


class GenerationsModel(Base):
    __tablename__ = "generations"

    id: Mapped[universal_id] = mapped_column(index=True)
    created_at: Mapped[created_at]

    tg_id: Mapped[str]
    style: Mapped[str]
    status_message: Mapped[int] = mapped_column(nullable=True)
    bot_init_id: Mapped[str] = mapped_column(nullable=True, default=None)
    log_message_id: Mapped[str] = mapped_column(default=None, nullable=True)
    gen_parameters: Mapped[str] = mapped_column(default=None, nullable=True)

    gpu_id: Mapped[str] = mapped_column(default=None, nullable=True)
    eta_seconds: Mapped[int] = mapped_column(default=None, nullable=True)

    status: Mapped[str]
    finish_at: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    error_message: Mapped[str] = mapped_column(default=None, nullable=True)
    by_vip_quota: Mapped[bool] = mapped_column(default=None, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "tg_id": self.tg_id,
            "style": self.style,
            "bot_init_id": self.bot_init_id,
            "log_message_id": self.log_message_id,
            "gpu_id": self.gpu_id,
            "eta_seconds": self.eta_seconds,
            "status": self.status,
            "finish_at": self.finish_at,
            "error_message": self.error_message,
        }
