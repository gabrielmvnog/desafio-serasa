from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, root_validator


class OrderIn(BaseModel):
    user_id: int = Field(..., example=1)
    item_description: str = Field(..., example="this is an order")
    item_quantity: int = Field(..., gt=0, example=1)
    item_price: Decimal = Field(..., decimal_places=2, example=10.00)
    total_value: Decimal = Field(..., decimal_places=2, example=10.00)

    @root_validator
    def check_total_value_match(cls, values):
        total = values.get("item_quantity") * values.get("item_price")
        if total != values.get("total_value"):
            raise ValueError("Total value dont match with item price and item quantity")

        return values

    class Config:
        extra = "forbid"


class OrderOut(OrderIn):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example=datetime(2023, 7, 1))
    updated_at: datetime | None = Field(..., example=datetime(2023, 7, 1))

    class Config:
        orm_mode = True
