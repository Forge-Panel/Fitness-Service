import asyncio

from models import Exercise, ExerciseCategory, ExerciseBodyPart
from models.utils import init_engine, SessionFactory, create_tables
from datetime import datetime


async def main():
    engine = init_engine('postgresql+asyncpg://db:db@localhost:5430/db')

    await create_tables(engine)

    exercises = (
        ("Running", "Running outdoors or on a treadmill for cardiovascular health.",
         "Maintain a steady pace, keeping your arms at a 90-degree angle, and focus on your breathing.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        ("Cycling", "Using a stationary bike or riding outdoors for cardio.",
         "Adjust the seat to a comfortable height, keep your back straight, and pedal at a consistent pace.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        ("Jump Rope", "A full-body cardio workout using a jump rope.",
         "Hold the handles with your wrists, keep your elbows close to your body, and jump with a steady rhythm.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        ("Rowing", "Using a rowing machine to improve cardiovascular and back strength.",
         "Sit with feet secured, grab the handle with both hands, extend your legs, and pull the handle to your chest.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        ("Stair Climber", "Using a stair climber machine for lower body cardio.",
         "Step naturally as you would on stairs, keeping a steady pace and using handrails for balance if needed.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        ("Swimming", "A full-body workout performed in water to increase heart rate.",
         "Use a stroke style you are comfortable with and maintain consistent breathing.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        ("Box Jumps", "Jumping onto a box or platform to build leg strength and endurance.",
         "Stand facing the box, squat down, and explode up to land softly on top, then step down.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS),
        ("Burpees", "A full-body, high-intensity workout.",
         "Start standing, squat down, kick your feet back, perform a push-up, and jump back to standing.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.FULL_BODY),
        ("Mountain Climbers", "A dynamic exercise to increase heart rate and strengthen the core.",
         "Start in a plank position, drive one knee to your chest, then alternate legs quickly.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.CORE),
        ("Elliptical", "Low-impact cardio workout on an elliptical machine.",
         "Set the resistance, keep a steady pace, and focus on even, balanced movements.",
         ExerciseCategory.CARDIO, ExerciseBodyPart.LEGS)
    )

    async with SessionFactory.get_session() as session:
        current_date = datetime.now()

        for exercise in exercises:
            obj = Exercise(
                name=exercise[0],
                description=exercise[1],
                instructions=exercise[2],
                category=exercise[3],
                body_part=exercise[4],
                created_at=current_date,
                last_modified=current_date
            )

            print(obj)

            session.add(obj)

        await session.commit()


if __name__ == '__main__':
    asyncio.run(main())
