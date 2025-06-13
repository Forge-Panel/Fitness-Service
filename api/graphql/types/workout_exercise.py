import strawberry

from models import WorkoutExercise
from models.utils import SessionFactory
from . import ExerciseType, WorkoutExerciseSet
from ..dataloaders import exercise_loader




@strawberry.experimental.pydantic.type(model=WorkoutExercise)
class WorkoutExerciseType:
    id: strawberry.ID

    sets: list[WorkoutExerciseSet]

    note: strawberry.auto

    @strawberry.field
    async def exercise(self) -> ExerciseType:
        return await exercise_loader.load(self.exercise_id)