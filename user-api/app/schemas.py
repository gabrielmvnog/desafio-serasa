from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    name: str
    cpf: str
    email: EmailStr
    phone_number: str


class UserOut(UserIn):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
