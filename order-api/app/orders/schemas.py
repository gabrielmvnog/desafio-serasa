from datetime import datetime

from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    user_id: int = Field(..., example=1)
    item_description: str = Field(..., example="this is an order")
    item_quantity: int = Field(..., example=1)
    item_price: int = Field(..., example=10.00)
    total_value: int = Field(..., example=10.00)


class OrderOut(OrderIn):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example=datetime(2023, 7, 1))
    updated_at: datetime | None = Field(..., example=datetime(2023, 7, 1))
