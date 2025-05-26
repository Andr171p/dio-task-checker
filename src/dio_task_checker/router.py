from fastapi import APIRouter, status

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from langgraph.graph.graph import CompiledGraph

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
async def check_task(task: Task, agent: FromDishka[CompiledGraph]) -> CheckedTask:
    response = await agent.ainvoke({"task": task})
    return CheckedTask.model_validate(response)
