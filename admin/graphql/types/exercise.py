import strawberry

from models import Exercise


@strawberry.experimental.pydantic.type(model=Exercise)
class ExerciseType:
    id: strawberry.ID
    name: strawberry.auto
    description: strawberry.auto
    instructions: strawberry.auto
    category: strawberry.auto
    body_part: strawberry.auto
    created_at: strawberry.auto
    last_modified: strawberry.auto
