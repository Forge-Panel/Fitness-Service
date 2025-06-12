from datetime import datetime

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field
from .utils import SessionFactory, BaseCRUD


class Workout(SQLModel, BaseCRUD['Workout'], table=True):
    __tablename__ = "workout"

    class Config:
        arbitrary_types_allowed = True

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    note: str

    started_on: datetime
    ended_on: datetime | None

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def start_new(cls, user_id: int, note: str):
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


    async def add_exercise(self, exercise_id: int, note: str):
        from .workout_exercise import WorkoutExercise

        return await WorkoutExercise.create_new(workout_id=self.id, exercise_id=exercise_id, note=note)

    async def remove_exercise(self, id: int):
        from .workout_exercise import WorkoutExercise

        return await WorkoutExercise.create_new(workout_id=self.id, exercise_id=exercise_id, note=note)


