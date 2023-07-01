from datetime import datetime


def create_order_in_data():
    return {
        "user_id": 1,
        "item_description": "Iphone 14",
        "item_quantity": 10,
        "item_price": 15000.00,
        "total_value": 150000.00,
    }


def create_order_out_data():
    return {
        **create_order_in_data(),
        "id": 1,
        "created_at": datetime(2023, 7, 1),
        "updated_at": datetime(2023, 7, 1),
    }
