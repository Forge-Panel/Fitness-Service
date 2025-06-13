import strawberry

from models import Workout, WorkoutExerciseSet

from ..dataloaders import workout_loader, workout_exercise_loader
from ..types import WorkoutType, WorkoutExerciseType, WorkoutExerciseSetInput
from .workout_exercise import WorkoutExerciseMutation


@strawberry.type
class WorkoutMutation:
    workout: strawberry.Private[Workout]

    def __init__(self, workout: Workout):
        self.workout = workout

    @strawberry.mutation
    async def finish(self) -> WorkoutType:
        await self.workout.finish()

        # Update cache
        workout_loader.prime(self.workout.id, self.workout)

        return self.workout

    @strawberry.mutation
    async def add_exercise(self, exercise_id: int, note: str | None = None, sets: list[WorkoutExerciseSetInput] = None) -> WorkoutExerciseType:
        workout_exercise = await self.workout.add_exercise(exercise_id, note, [WorkoutExerciseSet(reps=set.reps, weight=set.weight) for set in sets])

        # Update cache
        workout_exercise_loader.prime(workout_exercise.id, workout_exercise)

        return workout_exercise

    @strawberry.field
    async def exercise_by_id(self, id: int) -> WorkoutExerciseMutation | None:
        return WorkoutExerciseMutation(await workout_exercise_loader.load(id))

    @strawberry.field
    async def delete(self) -> None:
        # Clear cache
        workout_loader.clear(self.workout.id)

        await self.workout.delete_self()