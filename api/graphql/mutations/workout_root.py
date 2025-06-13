import strawberry

from models import Workout

from ..types import WorkoutType
from ..dataloaders import workout_loader
from .workout import WorkoutMutation


@strawberry.input
class WorkoutStartInput:
    note: str | None = strawberry.field(description="Note of the workout", default=None)

@strawberry.type
class WorkoutRootMutation:
    @strawberry.mutation
    async def start(
            self,
            input: WorkoutStartInput
    ) -> WorkoutType:
        workout = await Workout.start_new(
            user_id=1,
            note=input.note
        )

        # Insert into cache
        workout_loader.prime(workout.id, workout)

        return workout

    @strawberry.field
    async def by_id(self, id: int) -> WorkoutMutation:
        workout = await workout_loader.load(id)

        if workout.user_id != 1:
            raise Exception(f"Workout with id {id} was not found")

        return WorkoutMutation(workout)