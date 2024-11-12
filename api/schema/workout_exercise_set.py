from dataclasses import dataclass

from pydantic import BaseModel
from models import WorkoutExerciseSet


@dataclass
class ExerciseSetResponseSchema:
    weight: int
    reps: int

    @classmethod
    async def from_model(cls, workout_exercise_set: WorkoutExerciseSet):
        return cls(
            weight=workout_exercise_set.weight,
            reps=workout_exercise_set.reps
        )

    @classmethod
    async def from_models(cls, workout_exercise_sets: list[WorkoutExerciseSet]):
        output = []

        for exercise_set in workout_exercise_sets:
            output.append(await cls.from_model(exercise_set))

        return output


class ExerciseSetWriteSchema(BaseModel):
    weight: int
    reps: int