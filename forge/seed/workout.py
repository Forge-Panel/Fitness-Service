import asyncio
import os
import random
import time

import click
from models import Exercise, User, Workout, WorkoutExerciseSet
from models.utils import init_engine, create_tables


async def seed_workout():
    start_time = time.perf_counter()
    engine = init_engine(os.getenv('DATABASE_URL'))
    await create_tables(engine)

    print("Inserting Workouts...", end='')
    workout_data = [
        ("Morning Burn", "Follow this to warm up and sweat", ["jump_rope", "cycling", "burpees"]),
        ("Leg Day", "Do 3 rounds with short rest", ["box_jumps", "running", "stair_climber"]),
        ("Full Body Cardio", "Stay consistent with form", ["burpees", "rowing", "jump_rope"]),
        ("Endurance Boost", "Go at a steady pace", ["elliptical", "swimming", "running"]),
        ("Core Crusher", "Perform each exercise for 1 minute", ["mountain_climbers", "burpees", "rowing"]),
        ("Light Recovery", "Keep the intensity low", ["elliptical", "cycling"]),
        ("Sweat Session", "Do each for 45 seconds, rest 15", ["box_jumps", "burpees", "mountain_climbers"]),
        ("Quick Burner", "3 rounds of each", ["jump_rope", "burpees", "running"]),
        ("Upper Body Strength", "Focus on controlled movements and full range of motion.", ["bench_press", "dumbbell_curl", "lateral_raise"]),
        ("Leg Power", "3 sets of each exercise, rest 60 seconds between sets.", ["squat", "leg_press", "box_jumps"]),
        ("Total Strength", "A solid full-body session. Go heavy but stay safe.", ["deadlift", "bench_press", "squat"]),
        ("Arm Blast", "Pump your biceps and triceps. 3x12 reps.", ["dumbbell_curl", "cable_tricep_pushdown", "assisted_dip"]),
        ("Back & Core", "Keep form tight and engage the core on every rep.", ["pull_up", "mountain_climbers", "plank"]),
        ("Functional Fit", "Perform each for 40 seconds, rest 20 seconds.", ["kettlebell_swing", "burpees", "lateral_raise"]),
        ("Shoulder & Chest", "4 sets of 10 reps. Focus on upper body hypertrophy.", ["bench_press", "lateral_raise", "assisted_dip"]),
        ("Core & Stability", "Hold and breathe. Build endurance in your core.", ["plank", "mountain_climbers", "wall_sit"]),
        ("Machine Madness", "Use machines to isolate and train safely.", ["leg_press", "elliptical", "cable_tricep_pushdown"]),
        ("Quick Recovery Flow", "Gentle movements to promote blood flow and recovery.", ["cycling", "elliptical", "plank"])
    ]

    exercises = {exercise.name.lower().replace(' ', '_').replace('-', '_'): exercise for exercise in await Exercise.read_all()}

    users = await User.read_all()

    for name, desc, ex_keys in workout_data:
        user = random.choice(users)

        workout = await Workout.start_new(user.id, None)

        for key in ex_keys:
            await workout.add_exercise(exercises[key].id, None, [
                WorkoutExerciseSet(reps=8, weight=23),
                WorkoutExerciseSet(reps=10, weight=23),
                WorkoutExerciseSet(reps=12, weight=23)
            ])

        await workout.finish()


    end_time = time.perf_counter()

    print(f"Done! Inserted {len(workout_data)} records in {round(end_time - start_time, 2)} seconds.")


@click.command()
def workouts():
    asyncio.run(seed_workout())
