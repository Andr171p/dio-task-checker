from src.ai_agent.agent import Agent
from src.models import Task, CheckedTask


class TaskAssistant:
    def __init__(self, agent: Agent) -> None:
        self._ai_agent = agent

    async def check_task(self, task: Task) -> CheckedTask:
        checked_task = await self._ai_agent.generate(task)
        return CheckedTask.model_validate(checked_task)
