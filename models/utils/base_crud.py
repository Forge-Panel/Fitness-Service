from typing import TypeVar, Generic
from sqlalchemy import select
from .session_factory import SessionFactory

T = TypeVar("T", bound="BaseCRUD")


class BaseCRUD(Generic[T]):
    @classmethod
    async def read_all(cls: type[T], offset: int = 0, limit: int = 100, ) -> list[T]:
        query = select(cls).offset(offset).limit(limit)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()

    @classmethod
    async def get_by_id(cls: type[T], id: int) -> T:
        stmt = select(cls).where(cls.id == id)

        async with SessionFactory.get_session() as session:
            result = await session.execute(stmt)
            return result.scalar_one()

    @classmethod
    async def try_get_by_id(cls: type[T], id: int) -> T | None:
        query = select(cls).where(cls.id == id)

        async with SessionFactory.get_session() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def does_id_exist(cls: type[T], id: int) -> bool:
        return bool(await cls.try_get_by_id(id))

    async def delete_self(self):
        async with SessionFactory.get_session() as session:
            session.delete(self)

            await session.commit()
