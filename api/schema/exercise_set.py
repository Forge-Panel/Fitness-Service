from dataclasses import dataclass

from pydantic import BaseModel
from models import ExerciseSet


@dataclass
class ExerciseSetResponseSchema:
    weight: int
    reps: int

    @classmethod
    async def from_model(cls, exercise_set: ExerciseSet):
        return cls(
            weight=exercise_set.weight,
            reps=exercise_set.reps
        )

    @classmethod
    async def from_models(cls, exercise_sets: list[ExerciseSet]):
        output = []

        for exercise_set in exercise_sets:
            output.append(await cls.from_model(exercise_set))

        return output


class ExerciseSetWriteSchema(BaseModel):
    weight: int
    reps: int