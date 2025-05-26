from typing_extensions import TypedDict

from src.dio_task_checker.schemas import Task


class AgentState(TypedDict):
    task: Task
    rate: int
    comments: str
