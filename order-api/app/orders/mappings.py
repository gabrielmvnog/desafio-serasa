orders_mapping = {
    "properties": {
        "user_id": {"type": "integer"},
        "item_description": {"type": "text"},
        "item_quantity": {"type": "integer"},
        "item_price": {"type": "scaled_float", "scaling_factor": 100},
        "total_value": {"type": "scaled_float", "scaling_factor": 100},
        "created_at": {"type": "date_nanos"},
        "updated_at": {"type": "date_nanos"},
    }
}
