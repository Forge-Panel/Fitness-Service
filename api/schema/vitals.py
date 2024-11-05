from dataclasses import dataclass

from datetime import datetime

from models import Vitals, VitalsProperties


@dataclass
class VitalsResponseSchema:
    date: datetime
    heart_rate: int | None
    blood_pressure_systolic: int | None
    blood_pressure_diastolic: int | None
    oxygen_level: int | None

    @classmethod
    async def from_model(cls, vitals: Vitals):
        return cls(
            date=vitals.date,
            heart_rate=vitals.heart_rate,
            blood_pressure_systolic=vitals.blood_pressure_systolic,
            blood_pressure_diastolic=vitals.blood_pressure_diastolic,
            oxygen_level=vitals.oxygen_level,
        )

    @classmethod
    async def from_models(cls, vitals: list[Vitals]):
        output = []

        for vital in vitals:
            output.append(await cls.from_model(vital))

        return output


class VitalsWriteSchema(VitalsProperties):
    pass
