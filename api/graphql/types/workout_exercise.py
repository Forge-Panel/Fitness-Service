import strawberry

from models import WorkoutExercise, WorkoutExerciseSet
from models.utils import SessionFactory
from sqlmodel import select

from . import ExerciseType
from .workout_exercise_set import WorkoutExerciseSetType
from ..dataloaders import exercise_loader


@strawberry.experimental.pydantic.type(model=WorkoutExercise)
class WorkoutExerciseType:
    id: strawberry.auto

    note: strawberry.auto

    @strawberry.field
    async def exercise(self) -> ExerciseType:
        return await exercise_loader.load(self.exercise_id)

    @strawberry.field
    async def sets(self) -> list[WorkoutExerciseSetType]:
        async with SessionFactory.get_session() as session:
            query = (
                select(WorkoutExerciseSet)
                .where(WorkoutExerciseSet.workout_exercise_id == self.id)
            )
            results = await session.execute(query)
            return results.scalars().all()
