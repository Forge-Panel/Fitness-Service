import click
import asyncio
import os
from models import User
from models.utils import init_engine, create_tables


async def add_user():
    print("Creating new user...")
    name = input("Name: ")

    engine = init_engine(os.getenv('DATABASE_URL'))

    await create_tables(engine)

    await User.create_new(name=name)

    print("User added Successfully")


@click.command()
def user():
    asyncio.run(add_user())
