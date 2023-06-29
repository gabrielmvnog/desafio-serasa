import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    cpf: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
    created_at: datetime = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: datetime = mapped_column(DateTime(timezone=True), onupdate=func.now())
