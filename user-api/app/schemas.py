from datetime import datetime

from pydantic import UUID4, BaseModel


class UserIn(BaseModel):
    name: str
    cpf: str
    email: str
    phone_number: str


class UserOut(UserIn):
    id: UUID4
    created_at: datetime
    updated_at: datetime
