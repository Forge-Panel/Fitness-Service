from datetime import datetime

from sqlmodel import SQLModel, Field


class Workout(SQLModel, table=True):
    __tablename__ = "workout"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
