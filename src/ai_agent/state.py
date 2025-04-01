from typing_extensions import TypedDict

from src.models import Task


class State(TypedDict):
    task: Task
    rate: int
    comments: str
