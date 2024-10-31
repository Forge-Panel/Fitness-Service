from __future__ import annotations

from sqlmodel import SQLModel, Field, select
from .utils import SessionFactory


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)

    @classmethod
    async def read_all(cls, offset: int = 0, limit: int = 100):
        query = select(cls).offset(offset).limit(limit)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)

            return results.scalars().all()

    @classmethod
    async def get_by_id(cls, id: int) -> User:
        stmt = select(cls).where(cls.id == id)

        async with SessionFactory.get_session() as session:
            result = await session.execute(stmt)

            return result.scalar_one()

    @classmethod
    async def try_get_by_id(cls, id: int) -> User | None:
        query = select(cls).where(cls.id == id)

        async with SessionFactory.get_session() as session:
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def does_id_exist(cls, id: int) -> bool:
        return bool(await cls.try_get_by_id(id))

