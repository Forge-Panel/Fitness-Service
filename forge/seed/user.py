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
        User.create_new(name, email, password) for name, email, password in [
            ("Cathyleen Beston", "test@gmail.com", "1234"),
            ("Sigismond Yakovlev", "test@gmail.com", "1234"),
            ("Trevar Staniford", "test@gmail.com", "1234"),
            ("Frieda Welman", "test@gmail.com", "1234"),
            ("Meghann Glazyer", "test@gmail.com", "1234"),
            ("Amandy Beswell", "test@gmail.com", "1234"),
            ("Sharl Siman", "test@gmail.com", "1234"),
            ("Piper Lambell", "test@gmail.com", "1234"),
            ("Meridel Groundwator", "test@gmail.com", "1234"),
            ("Bucky Triplett", "test@gmail.com", "1234")
        ]
    ])

    end_time = time.perf_counter()

    print(f"Done! Inserted {len(users)} records in {round(end_time - start_time, 2)} seconds.")


@click.command()
def users():
    asyncio.run(seed_users())