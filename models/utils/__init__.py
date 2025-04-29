from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from .session_factory import SessionFactory
from .base_crud import BaseCRUD


def init_engine(database_url: str) -> AsyncEngine:
    engine = create_async_engine(database_url, echo=False, future=True)

    SessionFactory.inject_engine(engine)

    return engine


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
