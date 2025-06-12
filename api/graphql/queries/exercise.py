from sqlmodel import select

import strawberry

from ..dataloaders import exercise_loader
from ..types import ExerciseType

from models import Exercise, ExerciseCategory, ExerciseBodyPart
from models.utils import SessionFactory


@strawberry.type
class ExercisesQueries:
    @strawberry.field
    async def all(self, page: int = 1, count: int = 10, name: str | None = None, category: list[ExerciseCategory] | None = None, body_part: list[ExerciseBodyPart] | None = None) -> list[ExerciseType]:
        query = select(Exercise)

        if name:
            query = query.where(Exercise.name.contains(name))

        if category:
            query = query.where(Exercise.category.in_(category))

        if body_part:
            query = query.where(Exercise.body_part.in_(body_part))

        return await Exercise.read_all(
            page * count - count,
            count,
            query
        )

    @strawberry.field
    async def by_id(self, id: int) -> ExerciseType | None:
        return await exercise_loader.load(id)