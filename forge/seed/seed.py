import asyncio
import os
import random
import time

import click
from models import Exercise, ExerciseCategory, ExerciseBodyPart, User, WorkoutTemplate
from models.utils import init_engine, create_tables


async def run_seed():
    start_time = time.perf_counter()
    engine = init_engine(os.getenv('DATABASE_URL'))
    await create_tables(engine)

    print("Seeding database...")

    users = User.read_all()

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
    print("Done!")

    print("Inserting Workout templates...", end='')
    workout_templates_data = [
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

    for name, desc, ex_keys in workout_templates_data:
        user = random.choice(users)
        exs = [exercises[key] for key in ex_keys]
        await WorkoutTemplate.create_new(name, desc, user, exs)

    print("Done!")

    end_time = time.perf_counter()

    print(f"Finished, Inserted {len(users) + len(exercises_data) + len(workout_templates_data)} records in {round(end_time - start_time, 2)} seconds.")


@click.command()
def test_data():
    asyncio.run(run_seed())
