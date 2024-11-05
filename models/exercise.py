from __future__ import annotations

import typing

from sqlmodel import SQLModel, Field, Relationship, select
from .utils import BaseCRUD, SessionFactory

if typing.TYPE_CHECKING:
    from .exercise_set import ExerciseSet


class Exercise(SQLModel, BaseCRUD['Exercise'], table=True):
    __tablename__ = "exercise"

    id: int | None = Field(default=None, primary_key=True)

    workout_id: int = Field(primary_key=True, foreign_key="workout.id")
    exercise_template_id: int = Field(foreign_key="exercise_template.id")

    note: str

    @classmethod
    async def read_all_by_workout_id(cls, workout_id: int) -> list[Exercise]:
        query = select(cls).where(cls.workout_id == workout_id)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()

    async def fetch_sets(self) -> list[ExerciseSet]:
        from .exercise_set import ExerciseSet
        
        return await ExerciseSet.read_all_by_exercise_id(self.id)
