import asyncio
import os
import time

import click
from models import User
from models.utils import init_engine, create_tables


async def seed_users():
    start_time = time.perf_counter()
    engine = init_engine(os.getenv('DATABASE_URL'))
    await create_tables(engine)

    print("Inserting Users...", end='')
    users = await asyncio.gather(*[
        User.create_new(name) for name in [
            "Cathyleen Beston",
            "Sigismond Yakovlev",
            "Trevar Staniford",
            "Frieda Welman",
            "Meghann Glazyer",
            "Amandy Beswell",
            "Sharl Siman",
            "Piper Lambell",
            "Meridel Groundwator",
            "Bucky Triplett"
        ]
    ])

    end_time = time.perf_counter()

    print(f"Done! Inserted {len(users)} records in {round(end_time - start_time, 2)} seconds.")


@click.command()
def users():
    asyncio.run(seed_users())