from sqlmodel import select

import strawberry

from ..dataloaders import workout_loader
from ..types import WorkoutType

from models import Workout
from models.utils import SessionFactory


@strawberry.input
class WorkoutStartInput:
    note: str = strawberry.field(description="Note of the workout")


@strawberry.type
class WorkoutsQueries:
    @strawberry.field
    async def all(self, page: int = 1, count: int = 10) -> list[WorkoutType]:
        async with SessionFactory.get_session() as session:
            query = (
                select(Workout)
                .offset(page * count - count)
                .limit(count)
            )
            results = await session.execute(query)
            return results.scalars().all()

    @strawberry.field
    async def by_id(self, id: int) -> WorkoutType | None:
        return await workout_loader.load(id)