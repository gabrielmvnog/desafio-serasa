from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status

from app.dependencies import check_for_orders


@pytest.mark.anyio
@pytest.mark.usefixtures("mocked_httpx_get")
async def test_check_for_orders_should_pass(user_id):
    result = await check_for_orders(user_id)

    assert result is None


@pytest.mark.anyio
async def test_check_for_orders_should_raise_for_conflict(user_id, mocked_httpx_get):
    mocked_httpx_get.return_value = MagicMock(
        json=lambda: [{"order": "fake"}], status_code=status.HTTP_200_OK
    )

    with pytest.raises(HTTPException) as err:
        await check_for_orders(user_id)

    assert err.value.status_code == status.HTTP_409_CONFLICT
    assert err.value.detail == "User id [1] has orders"
