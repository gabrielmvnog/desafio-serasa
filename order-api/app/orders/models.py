from decimal import Decimal

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    item_description: Mapped[str]
    item_quantity: Mapped[int]
    item_price: Mapped[Decimal]
    total_value: Mapped[Decimal]
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
