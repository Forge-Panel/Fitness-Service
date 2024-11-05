from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class ExerciseTemplateProperties(BaseModel):
    name: str
    description: str


class ExerciseTemplate(SQLModel, ExerciseTemplateProperties, table=True):
    __tablename__ = "exercise_template"

    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
