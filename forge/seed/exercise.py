import asyncio
import os
import random
import time
import click
from models import Exercise, ExerciseCategory, ExerciseBodyPart, User, WorkoutTemplate
from models.utils import init_engine, create_tables


async def seed_exercises():
    start_time = time.perf_counter()
    engine = init_engine(os.getenv('DATABASE_URL'))
    await create_tables(engine)

    print("Inserting Exercises...", end='')
    exercises_data = {
        "running": ("Running", "Running outdoors or on a treadmill for cardiovascular health.",
                    "Maintain a steady pace...", ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        "cycling": ("Cycling", "Using a stationary bike or riding outdoors for cardio.",
                    "Adjust the seat...", ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        "jump_rope": ("Jump Rope", "A full-body cardio workout using a jump rope.",
                      "Hold the handles...", ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        "rowing": ("Rowing", "Using a rowing machine...",
                   "Sit with feet secured...", ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        "stair_climber": ("Stair Climber", "Using a stair climber machine...",
                          "Step naturally...", ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        "swimming": ("Swimming", "A full-body workout in water...",
                     "Use a stroke style...", ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        "box_jumps": ("Box Jumps", "Jumping onto a box...",
                      "Stand facing the box...", ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        "burpees": ("Burpees", "A full-body, high-intensity workout.",
                    "Start standing, squat...", ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        "mountain_climbers": ("Mountain Climbers", "Dynamic core exercise...",
                              "Start in plank...", ExerciseCategory.CARDIO, ExerciseBodyPart.CORE),
        "elliptical": ("Elliptical", "Low-impact cardio on elliptical machine.",
                       "Set the resistance...", ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        "bench_press": ("Bench Press", "Chest-focused strength exercise using a barbell.",
                        "Lie flat on a bench, grip bar slightly wider than shoulder-width...",
                        ExerciseCategory.BARBELL, ExerciseBodyPart.CHEST),
        "squat": ("Squat", "Compound leg exercise using a barbell or bodyweight.",
                  "Stand with feet shoulder-width apart, lower hips...",
                  ExerciseCategory.BARBELL, ExerciseBodyPart.LEGS),
        "deadlift": ("Deadlift", "Full-body strength lift using a barbell.",
                     "Stand with mid-foot under the barbell, bend at hips...",
                     ExerciseCategory.BARBELL, ExerciseBodyPart.FULL_BODY),
        "dumbbell_curl": ("Dumbbell Curl", "Isolated arm exercise using dumbbells.",
                          "Stand upright, curl weights toward shoulders...",
                          ExerciseCategory.DUMBBELL, ExerciseBodyPart.ARMS),
        "lateral_raise": ("Lateral Raise", "Shoulder-strengthening movement.",
                          "Raise dumbbells out to the sides to shoulder level...",
                          ExerciseCategory.DUMBBELL, ExerciseBodyPart.SHOULDERS),
        "kettlebell_swing": ("Kettlebell Swing", "Explosive hip-hinge workout using kettlebell.",
                             "Swing kettlebell between legs and up to chest level...",
                             ExerciseCategory.KETTLEBELL, ExerciseBodyPart.FULL_BODY),
        "leg_press": ("Leg Press", "Machine-based lower body exercise.",
                      "Push platform away with legs, don't lock knees...",
                      ExerciseCategory.MACHINE, ExerciseBodyPart.LEGS),
        "cable_tricep_pushdown": ("Cable Tricep Pushdown", "Triceps isolation with cable machine.",
                                  "Grip bar, elbows tucked in, extend arms downward...",
                                  ExerciseCategory.CABLE, ExerciseBodyPart.ARMS),
        "pull_up": ("Pull-Up", "Upper body compound movement using bodyweight.",
                    "Grip the bar with palms forward, pull chin above bar...",
                    ExerciseCategory.WEIGHTED_BODYWEIGHT, ExerciseBodyPart.BACK),
        "assisted_dip": ("Assisted Dip", "Triceps and chest exercise using assistance machine.",
                         "Lower yourself down and push up while knees rest on pad...",
                         ExerciseCategory.ASSISTED_BODY, ExerciseBodyPart.ARMS),
        "plank": ("Plank", "Isometric core-strengthening exercise.",
                  "Hold your body in a straight line, forearms on the ground...",
                  ExerciseCategory.DURATION, ExerciseBodyPart.CORE),
        "wall_sit": ("Wall Sit", "Isometric leg exercise held for time.",
                     "Slide down a wall until thighs are parallel to floor...",
                     ExerciseCategory.DURATION, ExerciseBodyPart.LEGS),
        "jumping_jacks": ("Jumping Jacks", "Cardio warm-up engaging full body.",
                          "Jump while spreading legs and arms overhead...",
                          ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY)
    }

    exercises = {}
    for key, (name, desc, instr, cat, part) in exercises_data.items():
        exercises[key] = await Exercise.create_new(name, desc, instr, cat, part)

    end_time = time.perf_counter()

    print(f"Done! Inserted {len(exercises_data)} records in {round(end_time - start_time, 2)} seconds.")


@click.command()
def exercises():
    asyncio.run(seed_exercises())
