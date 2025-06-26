from sqlmodel import select, asc, desc

import strawberry

from sharables.dataloaders import exercise_loader
from ..types import ExerciseType
from enum import Enum

from models import Exercise, ExerciseCategory, ExerciseBodyPart


@strawberry.enum
class ExerciseOrderByField(Enum):
    NAME = 'name'
    CATEGORY = "category"
    BODY_PART = "body_part"
    CREATED_AT = "created_at"
    LAST_MODIFIED = "last_modified"


@strawberry.enum
class ExerciseOrderByOrder(Enum):
    ASC = 'asc'
    DESC = "desc"


@strawberry.input
class ExerciseOrderBy:
    field: ExerciseOrderByField
    order: ExerciseOrderByOrder

@strawberry.type
class ExercisesQueries:
    @strawberry.field
    async def all(
            self,
            page: int = 1,
            count: int = 10,
            name: str | None = None,
            category: list[ExerciseCategory] | None = None,
            body_part: list[ExerciseBodyPart] | None = None,
            order_by: list[ExerciseOrderBy] | None = None,
    ) -> list[ExerciseType]:
        query = select(Exercise)

        if name:
            query = query.where(Exercise.name.contains(name))

        if category:
            query = query.where(Exercise.category.in_(category))

        if body_part:
            query = query.where(Exercise.body_part.in_(body_part))

        if order_by is not None:
            for order in order_by:
                query = query.order_by(asc(order.field.value) if order.order == ExerciseOrderByDirection.ASC else desc(order.field.value))

        return await Exercise.read_all(
            offset=page * count - count,
            limit=count,
            query=query
        )

    @strawberry.field
    async def by_id(self, id: int) -> ExerciseType | None:
        return await exercise_loader.load(id)