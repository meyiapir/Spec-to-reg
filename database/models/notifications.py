from __future__ import annotations

from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, universal_id


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[universal_id]
    creator_id: Mapped[str]
    text: Mapped[JSON] = mapped_column(JSON)
    media: Mapped[list[JSON]] = mapped_column(ARRAY(JSON))

    def to_str(self) -> str:
        return f"NotificationModel(id={self.id}, text={self.text}, media={str(self.media)})"
