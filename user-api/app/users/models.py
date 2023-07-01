from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy_utils.types.encrypted.encrypted_type import (
    AesEngine,
    StringEncryptedType,
)

from app.config import settings
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    cpf: Mapped[str] = mapped_column(
        StringEncryptedType(String, settings.SECRET_KEY, AesEngine, "pkcs5")
    )
    email: Mapped[str] = mapped_column(
        StringEncryptedType(String, settings.SECRET_KEY, AesEngine, "pkcs5")
    )
    phone_number: Mapped[str] = mapped_column(
        StringEncryptedType(String, settings.SECRET_KEY, AesEngine, "pkcs5")
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
