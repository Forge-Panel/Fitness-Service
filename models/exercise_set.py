from __future__ import annotations
from sqlmodel import SQLModel, Field, select

from .utils import SessionFactory


class ExerciseSet(SQLModel, table=True):
    __tablename__ = "exercise_set"

    id: int | None = Field(default=None, primary_key=True)

    exercise_id: int = Field(foreign_key="exercise.id")

    weight: int
    reps: int

    @classmethod
    async def read_all_by_exercise_id(cls, exercise_id: int) -> list[ExerciseSet]:
        query = select(cls).where(cls.exercise_id == exercise_id)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()
