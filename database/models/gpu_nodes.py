from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, created_at, universal_id

import datetime


class GpuNodeModel(Base):
    __tablename__ = "gpu_nodes"

    id: Mapped[universal_id]
    created_at: Mapped[created_at]

    tg_id: Mapped[str]
    name: Mapped[str]
    secret_key: Mapped[str]
    eta_seconds: Mapped[float] = mapped_column(nullable=True)
    is_pause: Mapped[bool] = mapped_column(default=True)
    status: Mapped[str]
    vip_coeff: Mapped[float] = mapped_column(default=0.5)
    processing_count: Mapped[int] = mapped_column(default=0)
    node_type: Mapped[str] = mapped_column(nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "tg_id": self.tg_id,
            "name": self.name,
            "host": self.host,
            "eta_seconds": self.eta_seconds,
            "is_active": self.is_active,
            "processings_count": self.processings_count,
            "processings_max": self.processings_max,
            "node_type": self.node_type,
        }
