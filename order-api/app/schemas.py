from datetime import datetime

from pydantic import BaseModel


class OrderIn(BaseModel):
    user_id: int
    item_description: str
    item_quantity: int
    item_price: int
    total_value: int


class OrderOut(OrderIn):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
