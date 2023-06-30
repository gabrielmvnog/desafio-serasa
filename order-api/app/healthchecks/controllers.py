from fastapi import APIRouter, status

router = APIRouter(tags=["healthchecks"])


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> dict[str, str]:
    return {"status": "ok"}
