from datetime import datetime

from app.schemas import UserIn, UserOut


def create_user_in_data():
    return UserIn(
        name="User Test",
        cpf="212.389.060-01",
        email="user_test@gmail.com",
        phone_number="(61)995637801",
    )


def create_user_out_data():
    return UserOut(
        **create_user_in_data().dict(),
        id=1,
        created_at=datetime(2023, 7, 1),
        updated_at=datetime(2023, 7, 1),
    )
