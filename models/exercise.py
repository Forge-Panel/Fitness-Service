from __future__ import annotations

from datetime import datetime

from .utils import BaseCRUD, SessionFactory
from sqlmodel import SQLModel, Field, select
from enum import Enum


class ExerciseCategory(str, Enum):
    BARBELL = "Barbell"
    DUMBBELL = "Dumbbell"
    KETTLEBELL = "Kettlebell"
    MACHINE = "Machine"
    CABLE = "Cable"
    WEIGHTED_BODYWEIGHT = "Weighted bodyweight"
    ASSISTED_BODY = "Assisted body"
    CARDIO = "Cardio"
    DURATION = "Duration"


class ExerciseBodyPart(str, Enum):
    CORE = "Core"
    ARMS = "Arms"
    BACK = "Back"
    CHEST = "Chest"
    LEGS = "Legs"
    SHOULDERS = "Shoulders"
    FULL_BODY = "Full body"
    OTHER = "Other"


class Exercise(SQLModel, BaseCRUD['Exercise'], table=True):
    __tablename__ = "exercise"

    id: int | None = Field(default=None, primary_key=True)
    
    name: str = Field(unique=True)
    description: str
    instructions: str
    category: ExerciseCategory
    body_part: ExerciseBodyPart

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def try_get_by_name(cls, name: str) -> Exercise | None:
        query = select(cls).where(cls.name == name)

        async with SessionFactory.get_session() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def does_name_exist(cls, name: str) -> bool:
        return bool(await cls.try_get_by_name(name))


    @classmethod
    async def create_new(cls, name: str, description: str, instructions: str, category: ExerciseCategory, body_part: ExerciseBodyPart)-> Exercise:
        current_date = datetime.now()

        if await Exercise.does_name_exist(name):
            raise Exception("Exercise name already exists")

        exercise = cls(
            name=name,
            description=description,
            category=category,
            instructions=instructions,
            body_part=body_part,
            created_at=current_date,
            last_modified=current_date
        )

        async with SessionFactory.get_session() as session:
            session.add(exercise)

            await session.commit()

            return exercise

    async def update_self(self, name: str, description: str, instructions: str, category: ExerciseCategory, body_part: ExerciseBodyPart)-> Exercise:

        if self.name != name and await Exercise.does_name_exist(name):
            raise Exception("Exercise name already exists")

        self.name = name
        self.description = description
        self.instructions = instructions
        self.category = category
        self.body_part = body_part
        self.last_modified = datetime.now()

        async with SessionFactory.get_session() as session:
            session.add(self)
            await session.commit()
            await session.refresh(self)
