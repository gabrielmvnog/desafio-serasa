from fastapi import FastAPI
from app.config import settings

from app.controllers import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
