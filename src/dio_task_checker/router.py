from fastapi import APIRouter, status

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from langchain_core.runnables import Runnable

from .schemas import Task, CheckedTask


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
async def check_task(task: Task, agent: FromDishka[Runnable]) -> CheckedTask:
    checked_task = await agent.ainvoke({
        "subdivision": task.subdivision,
        "theme": task.theme,
        "description": task.description,
        "hours": task.hours,
        "jobs": task.jobs
    })
    return checked_task
