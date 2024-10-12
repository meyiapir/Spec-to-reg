from sqlalchemy.orm import Mapped

from API.database.models.base import Base, created_at, universal_id


class StarsModel(Base):
    __tablename__ = "stars"
    order_id: Mapped[universal_id]
    user_id: Mapped[str]

    created_at: Mapped[created_at]

    price: Mapped[float]
    tariff: Mapped[str]
    count: Mapped[float]
