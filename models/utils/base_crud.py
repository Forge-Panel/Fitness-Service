from typing import TypeVar, Generic, Union
from sqlalchemy import select, Select
from .session_factory import SessionFactory

T = TypeVar("T", bound="BaseCRUD")


class BaseCRUD(Generic[T]):
    @classmethod
    async def read_all(cls: type[T], offset: int = 0, limit: int = 100, query: Select | None = None) -> list[T]:
        if query is None:
            query = select(cls)

        query = query.offset(offset).limit(limit)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)
            return results.scalars().all()

    @classmethod
    async def read_ids(cls: type[T], ids: list[int]) -> list[Union[T, Exception]]:
        async with SessionFactory.get_session() as session:
            results = await session.execute(select(cls).where(cls.id.in_(ids)))
            found_items = {item.id: item for item in results.scalars().all()}

        # Preserve input order and insert ValueError where missing
        return [found_items.get(id_, ValueError(f"{cls.__name__} with id {id_} not found")) for id_ in ids]

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

    async def update_self(self):
        async with SessionFactory.get_session() as session:
            session.add(self)

            await session.commit()

    async def delete_self(self):
        async with SessionFactory.get_session() as session:
            await session.delete(self)

            await session.commit()
