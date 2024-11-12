from fastapi import FastAPI
from .vitals import router as vitals_router
from .workout import router as workout_router
from .exercise import router as exercise_template_router

base_url = "/v1"


def init_routers(app: FastAPI):
    app.include_router(vitals_router, prefix=base_url)
    app.include_router(workout_router, prefix=base_url)
    app.include_router(exercise_template_router, prefix=base_url)
