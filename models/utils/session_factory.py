from contextlib import asynccontextmanager
from typing import Awaitable

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker


class SessionFactory:
    engine: AsyncEngine

    @classmethod
    def inject_engine(cls, engine: AsyncEngine):
        cls.engine = engine

    @classmethod
    @asynccontextmanager
    async def get_session(cls) -> Awaitable[AsyncSession]:
        async_session = sessionmaker(
            cls.engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session
