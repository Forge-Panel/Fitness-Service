import strawberry

from .workout import WorkoutRootMutation


@strawberry.type
class Mutation:
    workout: WorkoutRootMutation = strawberry.field(resolver=WorkoutRootMutation)
