from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, UniqueConstraint
from .utils import SessionFactory, BaseCRUD


class VitalsProperties(BaseModel):
    date: datetime
    heart_rate: int | None
    blood_pressure_systolic: int | None
    blood_pressure_diastolic: int | None
    oxygen_level: int | None


class Vitals(SQLModel, VitalsProperties, BaseCRUD['Vitals'], table=True):
    __tablename__ = "vitals"
    __table_args__ = (
        UniqueConstraint("user_id", "date", name="unique_vitals_date"),
    )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    @classmethod
    async def create_new(cls, user_id: int, properties: VitalsProperties) -> Vitals:
        vitals = cls(user_id=user_id, **properties.model_dump())

        # Ensure the vitals measurements are precise to the minute instead of second.
        vitals.date = vitals.date.replace(second=0, microsecond=0, tzinfo=None)

        async with SessionFactory.get_session() as session:
            session.add(vitals)

            await session.commit()

            return vitals
