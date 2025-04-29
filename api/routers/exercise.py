from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..services import ExerciseService
from ..schema.exercise import ExerciseResponseSchema, ExerciseWriteSchema


async def get_current_user() -> int:
    return 1


async def exercise_service_factory() -> ExerciseService:
    return ExerciseService(await get_current_user())


ExerciseServiceFactory = Annotated[ExerciseService, Depends(exercise_service_factory)]

router = APIRouter(prefix="/exercise", tags=["Exercise"])


@router.get("/all", description="Read all exercises.")
async def read_all_exercises(
        exercise_service: ExerciseServiceFactory,
        limit: int = 100,
        offset: int = 0
) -> list[ExerciseResponseSchema]:
    return await ExerciseResponseSchema.from_models(await exercise_service.read_all_exercises(offset, limit))


@router.post("/create", description="Create new exercise.", status_code=status.HTTP_201_CREATED)
async def create_new_exercise(
        exercise_service: ExerciseServiceFactory,
        schema: ExerciseWriteSchema
) -> ExerciseResponseSchema:
    return await ExerciseResponseSchema.from_model(await exercise_service.create_new_exercise(schema))


@router.get("/byId/{id}", description="Get the exercise by id.")
async def get_exercise_by_id(
        exercise_service: ExerciseServiceFactory,
        id: int
) -> ExerciseResponseSchema:
    return await ExerciseResponseSchema.from_model(await exercise_service.get_exercise_by_id(id))


@router.put("/byId/{id}", description="Update the exercise by id.", status_code=status.HTTP_201_CREATED)
async def update_exercise_by_id(
        exercise_service: ExerciseServiceFactory,
        id: int,
        schema: ExerciseWriteSchema
) -> ExerciseResponseSchema:
    return await ExerciseResponseSchema.from_model(await exercise_service.update_exercise_by_id(id, schema))


@router.delete("/byId/{id}", description="Delete the exercise by id.", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise_by_id(
        exercise_service: ExerciseServiceFactory,
        id: int
):
    await exercise_service.delete_exercise_by_id(id)
