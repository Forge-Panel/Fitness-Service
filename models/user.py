from __future__ import annotations

from datetime import datetime

from sqlmodel import SQLModel, Field, select
from .utils import SessionFactory


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)

    name: str

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)

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

    @classmethod
    async def does_name_exist(cls, name: str) -> bool:
        return bool(await cls.try_get_by_name(name))


    @classmethod
    async def create_new(cls, name: str)-> User:
        current_date = datetime.now()

        user = cls(
            name=name,
            created_at=current_date,
            last_modified=current_date
        )

        async with SessionFactory.get_session() as session:
            session.add(user)

            await session.commit()

            return user

