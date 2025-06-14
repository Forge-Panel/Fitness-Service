from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_database
from .graphql import init_graphql
from .cors import init_cors


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()

    yield


app = FastAPI(
    title="Forge-Fitness API",
    description="Official Fitness module for the Forge project. Includes everything about Vitals, Workout, Nutrition & Sleep.",
    lifespan=lifespan
)


# Init modules
init_cors(app)
init_graphql(app)
