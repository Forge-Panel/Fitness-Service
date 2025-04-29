from datetime import datetime

from sqlmodel import SQLModel, Field

from .workout_exercise import WorkoutExercise
from .utils import BaseCRUD


class Workout(SQLModel, BaseCRUD['Workout'], table=True):
    __tablename__ = "workout"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    note: str

    started_on: datetime
    ended_on: datetime

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)

    async def fetch_exercises(self) -> list[WorkoutExercise]:
        return await WorkoutExercise.read_all_by_workout_id(self.id)