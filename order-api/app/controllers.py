from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse

import app.services as services
from app.dependencies import validate_order
from app.exceptions import ConflictException, OrderNotFounException
from app.schemas import OrderIn, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.put("/{order_id}", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: Request, order_id: int, order_in: OrderIn = Depends(validate_order)
) -> OrderOut:
    try:
        response = services.create_order(order_in=order_in, order_id=order_id)
    except ConflictException:
        return RedirectResponse(request.url, status_code=status.HTTP_303_SEE_OTHER)

    return response


@router.post("/{order_id}")
async def update_order(order_id: int, order_in: OrderIn) -> None:
    response = services.update_order(order_in=order_in, order_id=order_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int) -> None:
    response = services.delete_order(order_id=order_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )


@router.get("/{order_id}")
async def detail_order(order_id: int) -> OrderOut:
    try:
        response = services.detail_order(order_id=order_id)
    except OrderNotFounException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        ) from None

    return response


@router.get("")
async def list_orders(order_id: int | None = Query(None)) -> list[OrderOut | None]:
    response = services.list_orders()

    return response
