import strawberry

from .workout_root import WorkoutRootMutation


@strawberry.type
class Mutation:
    workout: WorkoutRootMutation = strawberry.field(resolver=WorkoutRootMutation)
