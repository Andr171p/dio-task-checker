from typing import Union

from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel, LLM
from langchain_core.output_parsers import PydanticOutputParser

from src.ai_agent.state import State
from src.ai_agent.nodes.base_node import BaseNode
from src.ai_agent.format_instructions import RateJSON

from src.utils import read_txt
from src.settings import BASE_DIR


TEMPLATE_PATH = BASE_DIR / "prompts" / "Оценщик_заданий_сотруднику.txt"


class RateNode(BaseNode):
    def __init__(self, model: Union[BaseChatModel, LLM]) -> None:
        self._model = model

    def _create_chain(self) -> Runnable:
        parser = PydanticOutputParser(pydantic_object=RateJSON)
        prompt = (
            ChatPromptTemplate
            .from_messages([("system", read_txt(TEMPLATE_PATH))])
            .partial(format_instructions=parser.get_format_instructions())
        )
        return prompt | self._model | parser

    async def execute(self, state: State) -> dict:
        task = state.get("task")
        chain = self._create_chain()
        response = await chain.ainvoke(task.model_dump())
        rate = response.rate
        return {"task": task, "rate": rate}
