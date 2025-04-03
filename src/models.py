from pydantic import BaseModel


class Task(BaseModel):
    subdivision: str
    description: str
    hours: float


class CheckedTask(BaseModel):
    rate: int
    comments: str
