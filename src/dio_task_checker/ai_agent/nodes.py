from typing import Union
from typing_extensions import TypedDict

from abc import ABC, abstractmethod
import logging

from pydantic import BaseModel, Field

from langgraph.types import Command

from langchain_core.language_models import BaseChatModel

from .state import AgentState
from .templates import COMMENTS_TEMPLATE, RATE_TEMPLATE
from .utils import create_llm_chain, create_structured_output_llm_chain


class BaseNode(ABC):
    @abstractmethod
    async def __call__(self, state: TypedDict) -> Union[dict, Command]: pass


class CommentNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(COMMENTS_TEMPLATE, model)

    async def __call__(self, state: AgentState) -> dict[str, str]:
        self.logger.info("---COMMENT---")
        task = state["task"]
        comments = await self.llm_chain.ainvoke({
            "theme": task.theme,
            "subdivision": task.subdivision,
            "description": task.description,
            "hours": task.hours,
            "jobs": task.jobs
        })
        return {"comments": comments}


class TaskRate(BaseModel):
    rate: int = Field(
        description="Дай оценку от 1 до 10, где 10 идеально составленное задание, а 1 плохо составленное задание сотруднику"
    )


class RateNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_structured_output_llm_chain(
            schema=TaskRate,
            template=RATE_TEMPLATE,
            model=model
        )

    async def __call__(self, state: AgentState) -> dict[str, int]:
        self.logger.info("---RATE---")
        task = state["task"]
        task_rate: TaskRate = await self.llm_chain.ainvoke({
            "theme": task.theme,
            "subdivision": task.subdivision,
            "description": task.description,
            "hours": task.hours,
            "jobs": task.jobs
        })
        return {"rate": task_rate.rate}
