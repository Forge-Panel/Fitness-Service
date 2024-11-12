from dataclasses import dataclass

from datetime import datetime
from pydantic import BaseModel, Field
from models import Exercise, ExerciseCategory, ExerciseBodyPart


@dataclass
class ExerciseResponseSchema:
    id: int
    name: str
    description: str
    instructions: str
    category: ExerciseCategory
    body_part: ExerciseBodyPart
    created_at: datetime
    last_modified: datetime

    @classmethod
    async def from_model(cls, exercise: Exercise):
        return cls(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            instructions=exercise.instructions,
            category=exercise.category,
            body_part=exercise.body_part,
            created_at=exercise.created_at,
            last_modified=exercise.last_modified,
        )

    @classmethod
    async def from_models(cls, exercises: list[Exercise]):
        output = []

        for exercise in exercises:
            output.append(await cls.from_model(exercise))

        return output


class ExerciseWriteSchema(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=512)
    instructions: str = Field(max_length=4096)
    category: ExerciseCategory
    body_part: ExerciseBodyPart
