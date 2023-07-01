from typing import Generator

import httpx
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.db.session import SessionLocal
from app.orders.schemas import OrderIn

security = HTTPBearer()


async def validate_order(order_in: OrderIn):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_API_URL}/{order_in.user_id}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User id [{order_in.user_id}] is not valid",
        )

    return order_in


def authorizaton(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != settings.TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
