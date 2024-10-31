from fastapi import FastAPI
from .vitals import router as vitals_router

base_url = "/v1"


def init_routers(app: FastAPI):
    app.include_router(vitals_router, prefix=base_url)
