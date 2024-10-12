from __future__ import annotations

from sqlalchemy.orm import Mapped

from API.database.models.base import Base, universal_id


class ProcessingModel(Base):
    __tablename__ = "processings"

    id: Mapped[universal_id]
    pack_msg_id: Mapped[str]
    count: Mapped[int]
    price: Mapped[int]

    def to_str(self) -> str:
        return f"ProcessingModel(id={self.id}, pack_msg_id={self.pack_msg_id}, price={str(self.price)})"
