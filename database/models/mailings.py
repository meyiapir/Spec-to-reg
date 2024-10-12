from __future__ import annotations

from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, universal_id

from datetime import datetime


class MailingModel(Base):
    __tablename__ = "mailings"

    id: Mapped[universal_id]
    creator_id: Mapped[str]
    text: Mapped[JSON] = mapped_column(JSON)
    media: Mapped[list[JSON]] = mapped_column(ARRAY(JSON))
    time: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(default="waiting")

    def to_str(self) -> str:
        return f"MailingModel(id={self.id}, creator_id={self.creator_id}, text={self.text}, file_ids={str(self.media)}, time={self.time}, status={self.status})"
