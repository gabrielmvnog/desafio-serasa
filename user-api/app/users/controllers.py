from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

import app.users.services as services
from app.dependencies import check_for_orders, get_db
from app.examples import (
    RESPONSE_303_EXAMPLE,
    RESPONSE_404_EXAMPLE,
    RESPONSE_409_EXAMPLE,
    RESPONSE_422_EXAMPLE,
)
from app.users.exceptions import ConflictException, UserNotFounException
from app.users.schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.put(
    "/{user_id}",
    status_code=status.HTTP_201_CREATED,
    responses={**RESPONSE_303_EXAMPLE, **RESPONSE_422_EXAMPLE},
)
async def create_user(
    request: Request, user_id: int, user_in: UserIn, db: Session = Depends(get_db)
) -> UserOut:
    try:
        response = services.create_user(db, user_in=user_in, user_id=user_id)
    except ConflictException:
        return RedirectResponse(request.url, status_code=status.HTTP_303_SEE_OTHER)

    return response


@router.post(
    "/{user_id}",
    responses={**RESPONSE_404_EXAMPLE, **RESPONSE_422_EXAMPLE},
)
async def update_user(
    user_id: int, user_in: UserIn, db: Session = Depends(get_db)
) -> None:
    response = services.update_user(db, user_in=user_in, user_id=user_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**RESPONSE_404_EXAMPLE, **RESPONSE_422_EXAMPLE, **RESPONSE_409_EXAMPLE},
)
async def delete_user(
    user_id: int, db: Session = Depends(get_db), _: None = Depends(check_for_orders)
) -> None:
    response = services.delete_user(db, user_id=user_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get(
    "/{user_id}",
    responses={**RESPONSE_404_EXAMPLE, **RESPONSE_422_EXAMPLE},
)
@cache(expire=60)
async def detail_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    try:
        user = services.detail_user(db, user_id=user_id)
    except UserNotFounException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from None

    return user


@router.get("", responses=RESPONSE_422_EXAMPLE)
@cache(expire=60)
async def list_users(
    skip: int | None = Query(None, example=0),
    limit: int | None = Query(None, example=10),
    db: Session = Depends(get_db),
) -> list[UserOut | None]:
    user = services.list_users(db, skip=skip, limit=limit)

    return user
