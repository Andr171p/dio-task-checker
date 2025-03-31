from pydantic import BaseModel


class Task(BaseModel):
    partner: str
    subdivision: str
    description: str
    hours: float
