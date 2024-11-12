from dataclasses import dataclass

from pydantic import BaseModel, Field

from models import Exercise
from .workout_exercise_set import ExerciseSetResponseSchema, ExerciseSetWriteSchema


@dataclass
class ExerciseResponseSchema:
    note: str
    sets: list[ExerciseSetResponseSchema]

    @classmethod
    async def from_model(cls, exercise: Exercise):
        return cls(
            note=exercise.note,
            sets=await ExerciseSetResponseSchema.from_models(await exercise.fetch_sets())
        )

    @classmethod
    async def from_models(cls, exercises: list[Exercise]):
        output = []

        for exercise in exercises:
            output.append(await cls.from_model(exercise))

        return output


class ExerciseWriteSchema(BaseModel):
    note: str = Field(max_length=512)
    sets: list[ExerciseSetWriteSchema]