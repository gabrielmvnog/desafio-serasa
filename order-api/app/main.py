from fastapi import FastAPI

from app.orders.controllers import router
from app.healthchecks.controllers import router as healthchecks_router
from app.orders.controllers import router as orders_router

app = FastAPI()

app.include_router(healthchecks_router)
app.include_router(orders_router)
