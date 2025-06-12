import strawberry

from models import Workout

from datetime import datetime

from ..dataloaders import workout_loader
from ..types import WorkoutType

@strawberry.input
class WorkoutStartInput:
    note: str = strawberry.field(description="Note of the workout")


@strawberry.type
class WorkoutMutation:
    workout: strawberry.Private[Workout]

    def __init__(self, workout: Workout):
        self.workout = workout

    @strawberry.mutation
    async def finish(
            self
    ) -> WorkoutType:
        await self.workout.finish()
        print("Workout is finisuhed now")
        print(self.workout)

        workout_loader.clear(self.workout.id)

        return self.workout

    @strawberry.mutation
    async def add_exercise(
            self
    ) -> WorkoutType:
        await self.workout.finish()

        workout_loader.clear(self.workout.id)

        return self.workout


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

        workout_loader.prime(id, workout)

        return workout

    @strawberry.field
    async def by_id(self, id: int) -> WorkoutMutation | None:
        workout = await workout_loader.load(id)

        return WorkoutMutation(workout)