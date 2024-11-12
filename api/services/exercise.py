from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException, status
from sqlmodel import select

from api.schema.exercise import ExerciseWriteSchema
from models import Exercise
from models.utils import SessionFactory


class ExerciseService:
    def __init__(self, user_id: int):
        """
        Initializes the ExerciseService with a specific user ID.

        :param user_id: The ID of the user for whom the service will perform operations.
        """
        self.user_id = user_id

    async def read_all_exercises(self, offset: int = 0, limit: int = 100) -> List[Exercise]:
        """
        Retrieves all exercise with optional pagination.

        :param offset: The starting index for pagination.
        :param limit: The maximum number of exercise templates to return.
        :return: A list of Exercise objects.
        """
        async with SessionFactory.get_session() as session:
            query = (
                select(Exercise)
                .offset(offset)
                .limit(limit)
            )
            results = await session.execute(query)
            return results.scalars().all()

    async def create_new_exercise(self, exercise_schema: ExerciseWriteSchema) -> Exercise:
        """
        Creates a new exercise.

        :param exercise_schema: The schema of the exercise.
        :return: The created Exercise object.
        """

        if await Exercise.does_name_exist(exercise_schema.name):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Exercise name already exists")

        exercise = await Exercise.create_new(**exercise_schema.model_dump())

        return exercise

    async def get_exercise_by_id(self, id: int) -> Optional[Exercise]:
        """
        Retrieves an exercise by ID.

        :param id: The ID of the exercise template to retrieve.
        :return: The Exercise object if found, otherwise None.
        """
        exercise = await Exercise.try_get_by_id(id)
        if not exercise:
            return None
        return exercise

    async def update_exercise_by_id(self, id: int, exercise_schema: ExerciseWriteSchema) -> Optional[Exercise]:
        """
        Updates an existing exercise with new data.

        :param id: The ID of the exercise to update.
        :param exercise_schema: The schema of the exercise.
        :return: The updated Exercise object if successful, otherwise None.
        """
        exercise = await Exercise.try_get_by_id(id)

        if not exercise:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Exercise not found")

        if exercise.name != exercise_schema.name and await Exercise.does_name_exist(exercise_schema.name):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Exercise name already exists")

        await exercise.update(**exercise_schema.model_dump())

        return exercise

    async def delete_exercise_by_id(self, id: int) -> bool:
        """
        Deletes an exercise by ID.

        :param id: The ID of the exercise to delete.
        :return: True if the exercise was successfully deleted, False otherwise.
        """
        exercise = await Exercise.try_get_by_id(id)
        if not exercise:
            return False

        await exercise.delete_self()
        return True
