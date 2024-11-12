from typing import Optional, List

from sqlmodel import select
from models import Workout
from models.utils import SessionFactory
from datetime import datetime, timezone


class WorkoutService:
    def __init__(self, user_id: int):
        """
        Initializes the WorkoutService with a specific user ID.
        
        :param user_id: The ID of the user for whom the service will perform operations.
        """
        self.user_id = user_id

    async def create_new_workout(self, note: str, started_on: datetime, ended_on: datetime) -> Workout:
        """
        Creates a new workout entry for the user.

        :param note: Description or note for the workout.
        :param started_on: Timestamp when the workout started.
        :param ended_on: Timestamp when the workout ended.
        :return: The created Workout object.
        """

        current_date = datetime.now(timezone.utc)
        
        workout = Workout(
            user_id=self.user_id,
            note=note,
            started_on=started_on,
            ended_on=ended_on,
            created_at=current_date,
            last_modified=current_date
        )

        async with SessionFactory.get_session() as session:
            session.add(workout)
            await session.commit()
            await session.refresh(workout)

        return workout

    async def read_all_workouts(self, offset: int = 0, limit: int = 100) -> List[Workout]:
        """
        Retrieves all workouts for the user with optional pagination.

        :param offset: The starting index for pagination.
        :param limit: The maximum number of workouts to return.
        :return: A list of Workout objects.
        """
        async with SessionFactory.get_session() as session:
            query = (
                select(Workout)
                .where(Workout.user_id == self.user_id)
                .order_by(Workout.started_on.desc())
                .offset(offset)
                .limit(limit)
            )
            results = await session.execute(query)
            return results.scalars().all()

    async def get_workout_by_id(self, id: int) -> Optional[Workout]:
        """
        Fetches a specific workout by ID if it belongs to the user.

        :param id: The ID of the workout to retrieve.
        :return: The Workout object if found, otherwise None.
        """
        workout = await Workout.try_get_by_id(id)
        if not workout or workout.user_id != self.user_id:
            return None
        return workout

    async def update_workout_by_id(self, id: int, note: Optional[str] = None,
                                   started_on: Optional[datetime] = None, ended_on: Optional[datetime] = None) -> Optional[Workout]:
        """
        Updates an existing workout with new information if it belongs to the user.

        :param id: The ID of the workout to update.
        :param note: Updated note for the workout.
        :param started_on: Updated start time of the workout.
        :param ended_on: Updated end time of the workout.
        :return: The updated Workout object if successful, otherwise None.
        """
        workout = await Workout.try_get_by_id(id)
        if not workout:
            raise Exception(f'Workout with ID {id} does not exist.')
        
        if workout.user_id != self.user_id:
            raise Exception(f'Workout with ID {id} does not belong to the user {workout.user_id}.')

        if note is not None:
            workout.note = note
            
        if started_on is not None:
            workout.started_on = started_on
            
        if ended_on is not None:
            workout.ended_on = ended_on
            
        workout.last_modified = datetime.now(timezone.utc)

        async with SessionFactory.get_session() as session:
            session.add(workout)
            await session.commit()
            await session.refresh(workout)

        return workout

    async def delete_workout_by_id(self, id: int):
        """
        Deletes a workout by ID if it belongs to the user.

        :param id: The ID of the workout to delete.
        :return: True if the workout was successfully deleted, False otherwise.
        """
        workout = await Workout.try_get_by_id(id)

        if not workout:
            raise Exception(f'Workout with ID {id} does not exist.')

        if workout.user_id != self.user_id:
            raise Exception(f'Workout with ID {id} does not belong to the user {workout.user_id}.')


        await workout.delete_self()
