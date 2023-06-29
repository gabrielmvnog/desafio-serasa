from fastapi import APIRouter, HTTPException, status

import app.services as services
from app.exceptions import ConflictException
from app.schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/{user_id}", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_id: int, user: UserIn):
    try:
        response = services.create_user(user_id, user)
    except ConflictException:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, detail="User already exist"
        ) from None

    return response


@router.post("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserIn):
    response = services.update_user(user_id, user)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return response


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    response = services.delete_user(user_id=user_id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get("/{user_id}", response_model=UserOut)
async def detail_user(user_id: int):
    user = services.detail_user(user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.get("", response_model=list[UserOut | None])
async def list_users():
    user = services.list_users()

    return user
