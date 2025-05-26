from typing import Optional

from pydantic import BaseModel, Field, field_validator

from .constants import MIN_RATE, MAX_RATE


class Job(BaseModel):
    hours: float
    content: Optional[str]

    def to_text(self, index: int) -> str:
        pattern = """
        {index}. Количество часов: {hours}
        Содержание: {content}
        """
        return pattern.format(index=index, **self.model_dump())


class Task(BaseModel):
    subdivision: str
    theme: str
    description: Optional[str]
    hours: float
    jobs: Optional[list[Job]]

    @field_validator("jobs")
    def format_jobs_to_text(cls, jobs: list[Job]) -> str:
        return "\n\n".join([job.to_text(index + 1) for index, job in enumerate(jobs)])


class CheckedTask(BaseModel):
    rate: int = Field(ge=MIN_RATE, le=MAX_RATE, description="Итоговая оценка от 1 до 10")
    comments: str = Field(description="Комментарии и рекомендации по улучшению")
