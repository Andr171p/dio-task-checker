from typing_extensions import TypedDict

from src.core.entities import Task


class State(TypedDict):
    task: Task
    rate: int
    comments: str
