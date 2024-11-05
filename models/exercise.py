from datetime import datetime

from sqlmodel import SQLModel, Field


class Exercise(SQLModel, table=True):
    __tablename__ = "exercise"

    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
