import asyncio
import os
import random
import time
from datetime import datetime, timedelta

import click
from models import User, Vitals, VitalsProperties
from models.utils import init_engine, create_tables
import numpy as np

def generate_fake_vitals_for_day(
        start_date: datetime,
        num_points: int = 24
) -> list[VitalsProperties]:
    """
    Generate realistic fake vitals for a single day with time intervals.
    """
    times = [start_date + timedelta(minutes=1 * i) for i in range(num_points)]

    # Simulated circadian rhythm for heart rate: lower at night, peaks in day
    heart_rate_base = np.sin(np.linspace(-np.pi / 2, 3 * np.pi / 2, num_points)) * 10 + 70
    heart_rate = heart_rate_base + np.random.normal(0, 3, num_points)

    # Blood pressure varies slightly throughout the day
    systolic = np.clip(np.random.normal(120, 5, num_points), 105, 135)
    diastolic = np.clip(np.random.normal(80, 3, num_points), 65, 90)

    # Oxygen level is usually stable unless health issues
    oxygen = np.clip(np.random.normal(98, 1, num_points), 94, 100)

    vitals_data = []
    for i in range(num_points):
        vitals_data.append(VitalsProperties(
            date=times[i],
            heart_rate=int(round(heart_rate[i])),
            blood_pressure_systolic=int(round(systolic[i])),
            blood_pressure_diastolic=int(round(diastolic[i])),
            oxygen_level=int(round(oxygen[i]))
        ))

    return vitals_data


async def seed_vitals():
    start_time = time.perf_counter()
    engine = init_engine(os.getenv('DATABASE_URL'))
    await create_tables(engine)

    print("Generating Vitals data...", end='')
    print(end='')
    vitals_count = 0
    for user in await User.read_all():
        current_date = datetime.now()

        for vital in generate_fake_vitals_for_day(datetime(year=current_date.year, month=current_date.month, day=current_date.day, hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59)), random.randint(100, 1000)):
            await Vitals.create_new(user.id, vital)
            vitals_count += 1

    end_time = time.perf_counter()

    print(f"Done! Inserted {vitals_count} records in {round(end_time - start_time, 2)} seconds.")


@click.command()
def vitals():
    asyncio.run(seed_vitals())