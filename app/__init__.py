from fastapi import FastAPI
from contextlib import asynccontextmanager
from sharables.database import init_database
from sharables.cors import init_cors
from .graphql import init_graphql


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()

    yield


app = FastAPI(
    title="Forge-Fitness App API",
    description="Official Fitness module for the Forge project. Includes everything about Vitals, Workout, Nutrition & Sleep.",
    lifespan=lifespan
)


# Init modules
init_cors(app)
init_graphql(app)
