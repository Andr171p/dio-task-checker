from litestar import Controller, Router, post

from src.models import Task, CheckedTask
from src.task_assistant import TaskAssistant


class TaskController(Controller):
    path = "/task"

    @post()
    async def check_task(self, data: Task) -> CheckedTask:
        ...
