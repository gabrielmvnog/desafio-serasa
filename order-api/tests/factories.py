from datetime import datetime

from app.schemas import OrderIn, OrderOut


def create_order_in_data():
    return OrderIn(
        user_id=1,
        item_description="Iphone 14",
        item_quantity=10,
        item_price=15000.00,
        total_value=150000.00,
    )


def create_order_out_data():
    return OrderOut(
        **create_order_in_data().dict(),
        id=1,
        created_at=datetime(2023, 7, 1),
        updated_at=datetime(2023, 7, 1),
    )
