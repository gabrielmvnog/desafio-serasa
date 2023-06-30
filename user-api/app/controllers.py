from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

import app.services as services
from app.dependencies import get_db
from app.exceptions import ConflictException, UserNotFounException
from app.schemas import UserIn, UserOut
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request, user_id: int, user_in: UserIn, db: Session = Depends(get_db)
) -> UserOut:
    try:
        response = services.create_user(db, user_in=user_in, user_id=user_id)
    except ConflictException:
        return RedirectResponse(request.url, status_code=status.HTTP_303_SEE_OTHER)

    return response


@router.post("/{user_id}")
async def update_user(
    user_id: int, user_in: UserIn, db: Session = Depends(get_db)
) -> None:
    response = services.update_user(db, user_in=user_in, user_id=user_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    response = services.delete_user(db, user_id=user_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get("/{user_id}")
async def detail_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    try:
        user = services.detail_user(db, user_id=user_id)
    except UserNotFounException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from None

    return user


@router.get("")
async def list_users(db: Session = Depends(get_db)) -> list[UserOut | None]:
    user = services.list_users(db)

    return user
