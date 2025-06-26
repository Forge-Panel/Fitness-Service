from enum import Enum

import strawberry
from sqlmodel import select, asc, desc, or_

from sharables.dataloaders import user_loader
from ..types import UserType

from models import User


@strawberry.enum
class UserOrderByField(Enum):
    ID = 'id'
    NAME = 'name'
    EMAIL = "email"
    IS_PRIVATE = "is_private"
    PASSWORD = "password"
    CREATED_AT = "created_at"
    LAST_MODIFIED = "last_modified"


@strawberry.enum
class UserOrderByOrder(Enum):
    ASC = 'asc'
    DESC = "desc"


@strawberry.input
class UserOrderBy:
    field: UserOrderByField
    order: UserOrderByOrder


@strawberry.type
class UsersQueries:
    @strawberry.field
    async def all(self,
        page: int = 1,
        count: int = 10,
        search: str | None = None,
        order_by: list[UserOrderBy] | None = None,
    ) -> list[UserType]:
        query = select(User)

        if search:
            query = query.where(or_(
                User.name.like(search),
            ))

        if order_by is not None:
            for order in order_by:
                query = query.order_by(asc(order.field.value) if order.order == UserOrderByOrder.ASC else desc(order.field.value))

        return await User.read_all(
            offset=page * count - count,
            limit=count,
            query=query
        )

    @strawberry.field
    async def by_id(self, id: int) -> UserType | None:
        user = await User.get_by_id(id)

        if user.id != 1 and user.is_private:
            return None

        return user