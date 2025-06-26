from enum import Enum

from sqlmodel import select, asc, desc

import strawberry

from sharables.dataloaders import workout_loader
from ..types import WorkoutType

from models import Workout


@strawberry.input
class WorkoutStartInput:
    note: str = strawberry.field(description="Note of the workout")


@strawberry.enum
class WorkoutOrderByField(Enum):
    STARTED_ON = 'started_on'
    ENDED_ON = 'ended_on'
    CREATED_AT = "created_at"
    LAST_MODIFIED = "last_modified"


@strawberry.enum
class WorkoutOrderByOrder(Enum):
    ASC = 'asc'
    DESC = "desc"


@strawberry.input
class WorkoutOrderBy:
    field: WorkoutOrderByField
    order: WorkoutOrderByOrder


@strawberry.type
class WorkoutsQueries:
    @strawberry.field
    async def all(self, page: int = 1, count: int = 10, order_by: list[WorkoutOrderBy] | None = None) -> list[WorkoutType]:
        query = select(Workout).where(Workout.user_id == 1)

        if order_by is not None:
            for order in order_by:
                query = query.order_by(asc(order.field.value) if order.order == WorkoutOrderByOrder.ASC else desc(order.field.value))

        return await Workout.read_all(
            offset=page * count - count,
            limit=count,
            query=query
        )

    @strawberry.field
    async def by_id(self, id: int) -> WorkoutType | None:
        workout = await workout_loader.load(id)

        if workout.user_id != 1:
            return None

        return workout
