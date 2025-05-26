from typing import Optional

from pydantic import BaseModel, field_validator


class Job(BaseModel):
    hours: float
    content: Optional[str]

    def to_text(self) -> str:
        pattern = "Количество часов: {hours}; Содержание: {content}"
        return pattern.format(**self.model_dump())


class Task(BaseModel):
    subdivision: str
    theme: str
    description: Optional[str]
    hours: float
    jobs: Optional[list[Job]]

    @field_validator("jobs")
    def format_jobs_to_text(cls, jobs: list[Job]) -> str:
        return "\n".join([job.to_text() for job in jobs])


class CheckedTask(BaseModel):
    rate: int
    comments: str
