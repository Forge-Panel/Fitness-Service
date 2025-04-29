from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..services import WorkoutService
from ..schema.workout import WorkoutResponseSchema, WorkoutWriteSchema


async def get_current_user() -> int:
    return 1


async def workout_service_factory() -> WorkoutService:
    return WorkoutService(await get_current_user())


WorkoutServiceFactory = Annotated[WorkoutService, Depends(workout_service_factory)]

router = APIRouter(prefix="/workout", tags=["Workout"])


@router.get("/", description="Read all workouts.")
async def read_all_workouts(
        workout_service: WorkoutServiceFactory,
        limit: int = 100,
        offset: int = 0
) -> list[WorkoutResponseSchema]:
    return await WorkoutResponseSchema.from_models(await workout_service.read_all_workouts(offset, limit))


@router.post("/", description="Create new workout.", status_code=status.HTTP_201_CREATED)
async def create_new_workout(
        workout_service: WorkoutServiceFactory,
        schema: WorkoutWriteSchema
) -> WorkoutResponseSchema:
    return await WorkoutResponseSchema.from_model(await workout_service.create_new_workout(**schema.model_dump()))


@router.get("/{id}", description="Get the workout by id.")
async def get_workout_by_id(
        workout_service: WorkoutServiceFactory,
        id: int
) -> WorkoutResponseSchema:
    return await WorkoutResponseSchema.from_model(await workout_service.get_workout_by_id(id))


@router.put("/{id}", description="Update the workout by id.", status_code=status.HTTP_201_CREATED)
async def update_workout_by_id(
        workout_service: WorkoutServiceFactory,
        id: int,
        schema: WorkoutWriteSchema
) -> WorkoutResponseSchema:
    return await WorkoutResponseSchema.from_model(await workout_service.update_workout_by_id(id, **schema.model_dump()))


@router.delete("/{id}", description="Delete the workout by id.", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_by_id(
        workout_service: WorkoutServiceFactory,
        id: int
):
    await workout_service.delete_workout_by_id(id)
