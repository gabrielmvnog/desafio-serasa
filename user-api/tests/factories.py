from datetime import datetime


def create_user_in_data():
    return {
        "name": "User Test",
        "cpf": "21238906001",
        "email": "user_test@gmail.com",
        "phone_number": "+5521999999999",
    }


def create_user_out_data():
    return {
        **create_user_in_data(),
        "id": 1,
        "created_at": datetime(2023, 7, 1),
        "updated_at": datetime(2023, 7, 1),
    }
