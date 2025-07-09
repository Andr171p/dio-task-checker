from fastapi import APIRouter, status

from fastapi_cache.decorator import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from langchain_core.runnables import Runnable

from .schemas import Task, CheckedTask
from .constants import TTL


tasks_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    route_class=DishkaRoute
)


@tasks_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=CheckedTask
)
@cache(expire=TTL)
async def check_task(task: Task, agent: Depends[Runnable[dict[str, str | int], CheckedTask]]) -> CheckedTask:
    checked_task = await agent.ainvoke({
        "subdivision": task.subdivision,
        "theme": task.theme,
        "description": task.description,
        "hours": task.hours,
        "jobs": task.jobs
    })
    return checked_task
