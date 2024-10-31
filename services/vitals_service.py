from models.utils import SessionFactory
from models import Vitals, VitalsProperties
from sqlmodel import select
from datetime import datetime


class VitalsService:
    # This class provides methods to interact with vitals measurements for a specific user.
    user_id: int

    def __init__(self, user_id: int):
        # Initializes VitalsService with a user ID
        self.user_id = user_id

    async def read_all_vitals_measurement_between_range(self, start_date: datetime, end_date: datetime) -> list[Vitals]:
        """
        Retrieves all vitals measurements for the specified user within a date range.

        :param start_date: Start date for the range
        :param end_date: End date for the range
        :return: List of Vitals instances within the specified range
        """
        stmt = select(Vitals) \
            .where(Vitals.user_id == self.user_id) \
            .where(Vitals.date >= start_date) \
            .where(Vitals.date <= end_date)

        async with SessionFactory.get_session() as session:
            results = await session.execute(stmt)

            return results.scalars().all()

    async def get_one_vitals_measurement(self, date: datetime) -> Vitals:
        """
        Retrieves a single vitals measurement for the specified user on a specific date.

        :param date: Date of the measurement to retrieve
        :return: Vitals instance for the specified date
        """
        stmt = select(Vitals) \
            .where(Vitals.user_id == self.user_id) \
            .where(Vitals.date == date)

        async with SessionFactory.get_session() as session:
            # Execute the statement and return the single Vitals instance
            results = await session.execute(stmt)

            return results.scalar_one()

    async def create_new_vitals_measurement(self, properties: VitalsProperties) -> Vitals:
        """
        Creates a new vitals measurement for the specified user.

        :param properties: VitalsProperties instance containing vitals data
        :return: The newly created Vitals instance
        """
        # Creates a new Vitals record using the user_id and provided properties
        return await Vitals.create_new(self.user_id, properties)
