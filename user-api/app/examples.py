from fastapi import status

RESPONSE_303_EXAMPLE = {
    status.HTTP_303_SEE_OTHER: {"description": "Redirect to resource"}
}

RESPONSE_404_EXAMPLE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {"application/json": {"example": {"detail": "Object not found"}}},
    }
}


RESPONSE_409_EXAMPLE = {
    status.HTTP_409_CONFLICT: {
        "content": {"application/json": {"example": {"detail": "Conflict"}}},
    }
}

RESPONSE_422_EXAMPLE = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                    ]
                }
            }
        },
    }
}
