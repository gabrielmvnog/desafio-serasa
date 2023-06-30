from datetime import datetime

import phonenumbers
from pydantic import BaseModel, EmailStr, Field, validator
from validate_docbr import CPF

_cpf_validator = CPF()


class UserIn(BaseModel):
    name: str = Field(..., example="User Test")
    cpf: str = Field(..., min_length=11, max_length=11, example="21238906001")
    email: EmailStr = Field(..., example="user_test@gmail.com")
    phone_number: str = Field(..., example="+5521999999999")

    @validator("cpf")
    def validate_cpf(cls, v: str) -> str:
        is_valid = _cpf_validator.validate(v)

        if not is_valid:
            raise ValueError("Invalid CPF value")

        return v

    @validator("phone_number")
    def validate_phone_number(cls, v: str) -> str:
        is_valid = False

        try:
            parsed_value = phonenumbers.parse(v, None)
            is_valid = phonenumbers.is_valid_number(parsed_value)
        except phonenumbers.NumberParseException:
            pass

        if not is_valid:
            raise ValueError("Invalid phone number value")

        return v

    class Config:
        extra = "forbid"


class UserOut(UserIn):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example=datetime(2023, 7, 1))
    updated_at: datetime | None = Field(..., example=datetime(2023, 7, 1))

    class Config:
        orm_mode = True
