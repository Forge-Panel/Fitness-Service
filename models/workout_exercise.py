from __future__ import annotations

from sqlalchemy import Column, JSON

from .workout_exercise_set import WorkoutExerciseSet
from sqlmodel import SQLModel, Field, select
from .utils import BaseCRUD, SessionFactory


class WorkoutExercise(SQLModel, BaseCRUD['WorkoutExercise'], table=True):
    __tablename__ = "workout_exercise"

    class Config:
        arbitrary_types_allowed = True

    id: int | None = Field(default=None, primary_key=True)

    workout_id: int = Field(foreign_key="workout.id", ondelete="CASCADE")
    exercise_id: int = Field(foreign_key="exercise.id")

    sets: list[WorkoutExerciseSet] = Field(sa_column=Column(JSON), default_factory=list)

    note: str | None

    @classmethod
    async def read_all_by_workout_id(cls, workout_id: int) -> list[WorkoutExercise]:
        query = select(cls).where(cls.workout_id == workout_id)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()

    @classmethod
    async def create_new(cls, workout_id: int, exercise_id: int, note: str | None = None, sets: list[WorkoutExerciseSet] | None = None) -> WorkoutExercise:
        if sets is None:
            sets = []

        new_obj = cls(
            workout_id=workout_id,
            exercise_id=exercise_id,
            note=note,
            sets=[set.model_dump() for set in sets]
        )

        async with SessionFactory.get_session() as session:
            session.add(new_obj)

            await session.commit()

            return new_obj


    async def update_sets(self, sets: list[WorkoutExerciseSet]):
        self.sets = [set.model_dump() for set in sets]

        await self.update_self()