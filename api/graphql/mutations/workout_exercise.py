import strawberry

from models import WorkoutExercise, WorkoutExerciseSet

from ..types import WorkoutExerciseSetInput
from ..dataloaders import workout_exercise_loader


@strawberry.type
class WorkoutExerciseMutation:
    workout_exercise: strawberry.Private[WorkoutExercise]

    def __init__(self, workout_exercise: WorkoutExercise):
        self.workout_exercise = workout_exercise

    @strawberry.field
    async def update_sets(self, sets: list[WorkoutExerciseSetInput]) -> None:
        await self.workout_exercise.update_sets([WorkoutExerciseSet(reps=set.reps, weight=set.weight) for set in sets])

        workout_exercise_loader.prime(self.workout_exercise.id, self.workout_exercise)

    @strawberry.field
    async def delete(self) -> None:
        await self.workout_exercise.delete_self()

        # Clear cache
        workout_exercise_loader.clear(self.workout_exercise.id)
