import pytest

from app.users.schemas import UserIn
from tests.factories import create_user_in_data


@pytest.mark.parametrize(
    "value", ["testing@testing.com", "testing@gmail.com", "testing@yahoo.com"]
)
def test_schema_user_in_should_accept_valid_email(value):
    user = create_user_in_data()
    user["email"] = value

    user_in = UserIn.parse_obj(user)

    assert isinstance(user_in, UserIn)
    assert user_in.email == value


@pytest.mark.parametrize("value", ["testing", "testing@", "@testing.com"])
def test_schema_user_in_should_raise_for_invalid_email(value):
    user = create_user_in_data()
    user["email"] = value

    with pytest.raises(ValueError):
        UserIn.parse_obj(user)


@pytest.mark.parametrize("value", ["52497806012", "76459929050", "43769626001"])
def test_schema_user_in_should_accept_valid_cpf(value):
    user = create_user_in_data()
    user["cpf"] = value

    user_in = UserIn.parse_obj(user)

    assert isinstance(user_in, UserIn)
    assert user_in.cpf == value


@pytest.mark.parametrize(
    "value", ["437.696.260-01", "43769626002", "52497806013", "524978aaa06013"]
)
def test_schema_user_in_should_raise_for_invalid_cpf(value):
    user = create_user_in_data()
    user["cpf"] = value

    with pytest.raises(ValueError):
        UserIn.parse_obj(user)


@pytest.mark.parametrize("value", ["+442083661177", "+5521999999999"])
def test_schema_user_in_should_accept_valid_phone_number(value):
    user = create_user_in_data()
    user["phone_number"] = value

    user_in = UserIn.parse_obj(user)

    assert isinstance(user_in, UserIn)
    assert user_in.phone_number == value


@pytest.mark.parametrize("value", ["437.696.260-01", "43769626002", "52497806013"])
def test_schema_user_in_should_raise_for_invalid_phone_number(value):
    user = create_user_in_data()
    user["phone_number"] = value

    with pytest.raises(ValueError):
        UserIn.parse_obj(user)
