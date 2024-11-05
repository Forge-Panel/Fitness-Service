from __future__ import annotations

from datetime import datetime

from sqlmodel import SQLModel, Field
from .utils import BaseCRUD, SessionFactory


class WorkoutTemplate(SQLModel, BaseCRUD['WorkoutTemplate'], table=True):
    __tablename__ = "workout_template"

    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def create_new(cls, name: str, description: str, user_id: int) -> WorkoutTemplate:
        current_date = datetime.now()

        new_obj = cls(
            user_id=user_id,
            name=name,
            description=description,
            created_at=current_date,
            last_modified=current_date,
        )

        async with SessionFactory.get_session() as session:
            session.add(new_obj)

            await session.commit()

            return new_obj
