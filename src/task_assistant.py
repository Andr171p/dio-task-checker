from src.ai_agent import TaskAIAgent
from src.models import Task, CheckedTask


class TaskAssistant:
    def __init__(self, task_ai_agent: TaskAIAgent) -> None:
        self._task_ai_agent = task_ai_agent

    async def check_task(self, task: Task) -> CheckedTask:
        generated = await self._task_ai_agent.generate(task)
        return CheckedTask.model_validate(generated)
