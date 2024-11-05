from sqlmodel import SQLModel, Field


class WorkoutExercises(SQLModel, table=True):
    workout_id: int = Field(primary_key=True, foreign_key="workout.id")
    exercise_id: int = Field(primary_key=True, foreign_key="exercise.id")

