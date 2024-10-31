from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import init_routers
from .database import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()

    yield


app = FastAPI(lifespan=lifespan)


# Init modules
init_routers(app)
