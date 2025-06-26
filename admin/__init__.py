from fastapi import FastAPI
from contextlib import asynccontextmanager
from sharables.database import init_database
from sharables.cors import init_cors
from .config import config
from .graphql import init_graphql


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database(str(config.database_url))

    yield


app = FastAPI(
    title="Forge-Fitness Admin API",
    description="Official Fitness module for the Forge project. Includes everything about Vitals, Workout, Nutrition & Sleep.",
    lifespan=lifespan
)



# Init modules
init_cors(app, config.cors_allowed_domains)
init_graphql(app)
