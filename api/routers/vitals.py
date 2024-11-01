from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from services import VitalsService
from ..schema.vitals import VitalsResponseSchema, VitalsWriteSchema


async def get_current_user() -> int:
    return 1


router = APIRouter(prefix="/vitals", tags=["Vitals"])


@router.get("/read_range", description="Read a range of measurements between 2 points in time.")
async def read_vitals(
        user_id: Annotated[int, Depends(get_current_user)],
        start_date: datetime,
        end_date: datetime
) -> list[VitalsResponseSchema]:
    service = VitalsService(user_id)

    return VitalsResponseSchema.from_models(
        await service.read_all_vitals_measurement_between_range(start_date, end_date))


@router.get("/get_one", description="Get one vitals measurement, based on a certain datetime precise to the minute")
async def get_vitals(
        user_id: Annotated[int, Depends(get_current_user)],
        date: datetime
) -> VitalsResponseSchema:
    service = VitalsService(user_id)

    return VitalsResponseSchema.from_model(await service.get_one_vitals_measurement(date))


@router.post("/add_measurement", status_code=201, description="Add a new vitals measurement")
async def add_measurement(
        user_id: Annotated[int, Depends(get_current_user)],
        measurements: VitalsWriteSchema
) -> VitalsResponseSchema:
    service = VitalsService(user_id)

    return VitalsResponseSchema.from_model(await service.create_new_vitals_measurement(measurements))
