from __future__ import annotations
from sqlmodel import SQLModel, Field, select

from .utils import BaseCRUD, SessionFactory


class WorkoutExerciseSet(SQLModel, BaseCRUD['WorkoutExerciseSet'], table=True):
    __tablename__ = "workout_exercise_set"

    id: int | None = Field(default=None, primary_key=True)

    workout_exercise_id: int = Field(foreign_key="workout_exercise.id")

    distance: int | None = None
    weight: int | None = None
    time: int | None = None
    reps: int | None = None

    @classmethod
    async def read_all_by_workout_exercise_id(cls, workout_exercise_id: int) -> list[WorkoutExerciseSet]:
        query = select(cls).where(cls.workout_exercise_id == workout_exercise_id)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()
