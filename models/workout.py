from __future__ import annotations

from datetime import datetime

from sqlmodel import SQLModel, Field, select
from .utils import SessionFactory, BaseCRUD
from .workout_exercise_set import WorkoutExerciseSet


class Workout(SQLModel, BaseCRUD['Workout'], table=True):
    __tablename__ = "workout"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")

    note: str | None = None

    started_on: datetime
    ended_on: datetime | None

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def get_active_workout(cls, user_id: int) -> Workout | None:
        async with SessionFactory.get_session() as session:
            query = select(cls) \
                .where(
                cls.user_id == user_id,
                cls.ended_on == None
            )

            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def has_active_workout_by_user_id(cls, user_id: int) -> bool:
        active_workout = await cls.get_active_workout(user_id)

        return bool(active_workout)

    @classmethod
    async def start_new(cls, user_id: int, note: str | None = None):
        if await cls.has_active_workout_by_user_id(user_id):
            raise Exception("User already has an active workout")

        new_obj = cls(
            user_id=user_id,
            note=note,
            started_on=datetime.now()
        )

        async with SessionFactory.get_session() as session:
            session.add(new_obj)

            await session.commit()

            return new_obj

    async def finish(self):
        if self.ended_on is not None:
            raise Exception("Workout already finished")

        async with SessionFactory.get_session() as session:
            current_date = datetime.now()

            self.ended_on = current_date
            self.last_modified = current_date

            session.add(self)

            await session.commit()

    async def add_exercise(self, exercise_id: int, note: str | None = None, sets: list[WorkoutExerciseSet] | None = None):
        from .workout_exercise import WorkoutExercise

        return await WorkoutExercise.create_new(workout_id=self.id, exercise_id=exercise_id, note=note, sets=sets)
