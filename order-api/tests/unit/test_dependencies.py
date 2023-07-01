from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status

from app.dependencies import validate_order


@pytest.mark.anyio
@pytest.mark.usefixtures("mocked_httpx_get")
async def test_validate_order_should_return_order(order_in_data):
    order = await validate_order(order_in_data)

    assert order


@pytest.mark.anyio
async def test_validate_order_should_raise_for_bad_request(
    mocked_httpx_get, order_in_data
):
    mocked_httpx_get.return_value = MagicMock(status_code=status.HTTP_404_NOT_FOUND)

    order_in_data.user_id = 2

    with pytest.raises(HTTPException) as err:
        await validate_order(order_in_data)

    assert err.value.status_code == status.HTTP_400_BAD_REQUEST
    assert err.value.detail == "User id [2] is not valid"
