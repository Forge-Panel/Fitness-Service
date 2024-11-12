from sqlmodel import SQLModel, Field


class WorkoutTemplateExercises(SQLModel, table=True):
    __tablename__ = "workout_template_exercises"

    workout_template_id: int = Field(primary_key=True, foreign_key="workout_template.id")
    exercise_id: int = Field(primary_key=True, foreign_key="exercise.id")

