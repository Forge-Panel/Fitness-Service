import asyncio
import time

import click
from .user import users, seed_users
from .exercise import exercises, seed_exercises
from .workout_template import workout_templates, seed_workout_templates
from .vitals import vitals, seed_vitals


@click.group()
def seed():
    pass


seed.add_command(users)
seed.add_command(exercises)
seed.add_command(workout_templates)
seed.add_command(vitals)

@seed.command()
def all():
    print("Seeding database...")

    asyncio.run(seed_users())
    asyncio.run(seed_exercises())
    asyncio.run(seed_workout_templates())
    asyncio.run(seed_vitals())

    print("Done.")
