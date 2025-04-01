from litestar import Controller, post
from dishka.integrations.litestar import inject
from dishka.integrations.base import FromDishka

from src.models import Task, CheckedTask
from src.task_assistant import TaskAssistant


class TaskController(Controller):
    path = "/api/v1/tasks"

    @post()
    @inject
    async def check_task(
            self,
            data: Task,
            task_assistant: FromDishka[TaskAssistant]
    ) -> CheckedTask:
        checked_task = await task_assistant.check_task(data)
        return checked_task
