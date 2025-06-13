from pydantic import BaseModel, Field


class WorkoutExerciseSet(BaseModel):
    reps: int = Field(gt=0, le=1000, description="Number of reps")
    weight: float = Field(gt=0, le=1000, description="Weight in kg")