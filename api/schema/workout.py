from dataclasses import dataclass

from datetime import datetime
from pydantic import BaseModel, Field
from models import Workout
from .exercise import ExerciseResponseSchema, ExerciseWriteSchema


@dataclass
class WorkoutResponseSchema:
    id: int
    note: str
    started_on: datetime
    ended_on: datetime
    exercises: list[ExerciseResponseSchema]
    created_at: datetime
    last_modified: datetime

    @classmethod
    async def from_model(cls, workout: Workout):
        return cls(
            id=workout.id,
            note=workout.note,
            started_on=workout.started_on,
            ended_on=workout.ended_on,
            exercises=await ExerciseResponseSchema.from_models(await workout.fetch_exercises()),
            created_at=workout.created_at,
            last_modified=workout.last_modified,
        )

    @classmethod
    async def from_models(cls, vitals: list[Workout]):
        output = []

        for vital in vitals:
            output.append(await cls.from_model(vital))

        return output


class WorkoutWriteSchema(BaseModel):
    note: str = Field(max_length=512)
    started_on: datetime = Field(default_factory=datetime.now)
    ended_on: datetime
    exercises: list[ExerciseWriteSchema]
