from models.utils import init_engine, create_tables
from app.config import config


async def init_database():
    engine = init_engine(str(config.database_url))

    await create_tables(engine)
