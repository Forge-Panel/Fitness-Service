import strawberry

from sharables.dataloaders import user_loader
from ..types import UserType

from models import User

@strawberry.type
class UsersQueries:
    @strawberry.field
    async def me(self) -> UserType:
        return await user_loader.load(1)

    @strawberry.field
    async def by_id(self, id: int) -> UserType | None:
        user = await User.get_by_id(id)

        if user.id != 1 and user.is_private:
            return None

        return user