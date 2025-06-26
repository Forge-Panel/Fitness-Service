from models.utils import init_engine, create_tables


async def init_database(database_url: str):
    engine = init_engine(database_url)

    await create_tables(engine)
