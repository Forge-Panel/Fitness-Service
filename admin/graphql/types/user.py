import strawberry

from models import User


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.ID
    name: strawberry.auto
    is_private: strawberry.auto
    created_at: strawberry.auto
    last_modified: strawberry.auto
