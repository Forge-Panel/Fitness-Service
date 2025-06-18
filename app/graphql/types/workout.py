import strawberry

from models import Workout, WorkoutExercise

from models.utils import SessionFactory
from sqlmodel import select

from .workout_exercise import WorkoutExerciseType

@strawberry.experimental.pydantic.type(model=Workout)
class WorkoutType:
    id: strawberry.ID

    user_id: strawberry.auto

    note: strawberry.auto

    started_on: strawberry.auto
    ended_on: strawberry.auto

    created_at: strawberry.auto
    last_modified: strawberry.auto

    @strawberry.field
    async def exercises(self) -> list[WorkoutExerciseType]:
        async with SessionFactory.get_session() as session:
            query = (
                select(WorkoutExercise)
                .where(WorkoutExercise.workout_id == self.id)
            )
            results = await session.execute(query)
            return results.scalars().all()