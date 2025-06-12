import strawberry

from models import WorkoutExerciseSet
from models.utils import SessionFactory


@strawberry.experimental.pydantic.type(model=WorkoutExerciseSet)
class WorkoutExerciseSetType:
    id: strawberry.auto

    distance: strawberry.auto
    weight: strawberry.auto
    time: strawberry.auto
    reps: strawberry.auto
