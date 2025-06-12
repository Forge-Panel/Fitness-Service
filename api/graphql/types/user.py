import strawberry

from models import User


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto
    created_at: strawberry.auto
    last_modified: strawberry.auto
