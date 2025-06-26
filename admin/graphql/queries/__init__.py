import strawberry

from .exercise import ExercisesQueries
from .user import UsersQueries
from .workout import WorkoutsQueries


@strawberry.type
class Query:
    exercises: ExercisesQueries = strawberry.field(resolver=ExercisesQueries)
    workouts: WorkoutsQueries = strawberry.field(resolver=WorkoutsQueries)
    users: UsersQueries = strawberry.field(resolver=UsersQueries)
