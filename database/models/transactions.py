from __future__ import annotations

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from API.database.models.base import Base, universal_id, created_at


class TransactionModel(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[universal_id]
    created_at: Mapped[created_at]
    last_updated_at: Mapped[created_at]
    t_type: Mapped[str]
    sender_id: Mapped[str]
    receiver_id: Mapped[str]
    status: Mapped[str]
    amount: Mapped[int]
    vip: Mapped[bool]
    params: Mapped[JSON] = mapped_column(JSON)
