from fastapi import APIRouter, status

router = APIRouter(tags=["healthchecks"])


@router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"application/json": {"example": {"status": "ok"}}},
        }
    },
)
async def ping() -> dict[str, str]:
    return {"status": "ok"}
