from __future__ import annotations

import typing

from sqlmodel import SQLModel, Field, Relationship, select
from .utils import BaseCRUD, SessionFactory

if typing.TYPE_CHECKING:
    from .workout_exercise_set import WorkoutExerciseSet


class WorkoutExercise(SQLModel, BaseCRUD['WorkoutExercise'], table=True):
    __tablename__ = "workout_exercise"

    id: int | None = Field(default=None, primary_key=True)

    workout_id: int = Field(foreign_key="workout.id")
    exercise_id: int = Field(foreign_key="exercise.id")

    note: str

    @classmethod
    async def read_all_by_workout_id(cls, workout_id: int) -> list[WorkoutExercise]:
        query = select(cls).where(cls.workout_id == workout_id)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()

    async def fetch_sets(self) -> list[WorkoutExerciseSet]:
        from .workout_exercise_set import WorkoutExerciseSet
        
        return await WorkoutExerciseSet.read_all_by_workout_exercise_id(self.id)

    @classmethod
    async def create_new(cls, workout_id: int, exercise_id: int, note: str) -> WorkoutExercise:
        new_obj = cls(
            workout_id=workout_id,
            exercise_id=exercise_id,
            note=note
        )

        async with SessionFactory.get_session() as session:
            session.add(new_obj)

            await session.commit()

            return new_obj
