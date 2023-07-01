from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

import app.orders.services as services
from app.dependencies import get_db, validate_order
from app.examples import (
    RESPONSE_303_EXAMPLE,
    RESPONSE_400_EXAMPLE,
    RESPONSE_404_EXAMPLE,
    RESPONSE_422_EXAMPLE,
)
from app.orders.exceptions import ConflictException, OrderNotFounException
from app.orders.schemas import OrderIn, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.put(
    "/{order_id}",
    status_code=status.HTTP_201_CREATED,
    responses={**RESPONSE_422_EXAMPLE, **RESPONSE_400_EXAMPLE, **RESPONSE_303_EXAMPLE},
)
async def create_order(
    request: Request,
    order_id: int,
    order_in: OrderIn = Depends(validate_order),
    db: Session = Depends(get_db),
) -> OrderOut:
    try:
        response = services.create_order(db, order_in=order_in, order_id=order_id)
    except ConflictException:
        return RedirectResponse(request.url, status_code=status.HTTP_303_SEE_OTHER)

    return response


@router.post(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    responses={**RESPONSE_422_EXAMPLE, **RESPONSE_404_EXAMPLE},
)
async def update_order(
    order_id: int, order_in: OrderIn, db: Session = Depends(get_db)
) -> None:
    response = services.update_order(db, order_in=order_in, order_id=order_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPONSE_404_EXAMPLE,
)
async def delete_order(order_id: int, db: Session = Depends(get_db)) -> None:
    response = services.delete_order(db, order_id=order_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )


@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    responses={**RESPONSE_404_EXAMPLE, **RESPONSE_422_EXAMPLE},
)
@cache(expire=60)
async def detail_order(order_id: int, db: Session = Depends(get_db)) -> OrderOut:
    try:
        response = services.detail_order(db, order_id=order_id)
    except OrderNotFounException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        ) from None

    return response


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses=RESPONSE_422_EXAMPLE
)
@cache(expire=60)
async def list_orders(
    user_id: int | None = Query(None),
    skip: int | None = Query(None),
    limit: int | None = Query(None),
    db: Session = Depends(get_db),
) -> list[OrderOut | None]:
    response = services.list_orders(db, user_id=user_id, skip=skip, limit=limit)

    return response
