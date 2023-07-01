from typing import Generator

import httpx
from fastapi import HTTPException, status

from app.config import settings
from app.db.session import SessionLocal


async def check_for_orders(user_id: int) -> None:
    async with httpx.AsyncClient(timeout=settings.ORDER_API_TIMEOUT) as client:
        response = await client.get(settings.ORDER_API_URL, params={"user_id": user_id})

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Orders API is not responding",
        )

    if len(response.json()) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User id [{user_id}] has orders",
        )


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
