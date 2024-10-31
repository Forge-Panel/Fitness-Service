from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select, UniqueConstraint
from .utils import SessionFactory


class VitalsProperties(BaseModel):
    date: datetime
    heart_rate: int | None
    blood_pressure_systolic: int | None
    blood_pressure_diastolic: int | None
    oxygen_level: int | None


class Vitals(SQLModel, VitalsProperties, table=True):
    __tablename__ = "vitals"
    __table_args__ = (
        UniqueConstraint("user_id", "date", name="unique_vitals_date"),
    )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    @classmethod
    async def read_all(cls, offset: int = 0, limit: int = 100):
        query = select(cls).offset(offset).limit(limit)

        async with SessionFactory.get_session() as session:
            results = await session.execute(query)

            return results.scalars().all()

    @classmethod
    async def get_by_id(cls, id: int) -> Vitals:
        stmt = select(cls).where(cls.id == id)

        async with SessionFactory.get_session() as session:
            result = await session.execute(stmt)

            return result.scalar_one()

    @classmethod
    async def try_get_by_id(cls, id: int) -> Vitals | None:
        query = select(cls).where(cls.id == id)

        async with SessionFactory.get_session() as session:
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def does_id_exist(cls, id: int) -> bool:
        return bool(await cls.try_get_by_id(id))

    @classmethod
    async def create_new(cls, user_id: int, properties: VitalsProperties) -> Vitals:
        vitals = cls(user_id=user_id, **properties.model_dump())

        vitals.date = vitals.date.replace(second=0, microsecond=0, tzinfo=None)

        async with SessionFactory.get_session() as session:
            session.add(vitals)

            await session.commit()

            return vitals
