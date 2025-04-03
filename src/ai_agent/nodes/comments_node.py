from typing import Union

from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel, LLM

from src.ai_agent.state import State
from src.ai_agent.nodes.base_node import BaseNode

from src.utils import read_txt
from src.settings import BASE_DIR


TEMPLATE_PATH = BASE_DIR / "prompts" / "Комментатор_заданий_сотруднику.txt"


class CommentsNode(BaseNode):
    def __init__(self, model: Union[BaseChatModel, LLM]) -> None:
        self._model = model

    def _create_chain(self) -> Runnable:
        prompt = ChatPromptTemplate.from_template(read_txt(TEMPLATE_PATH))
        parser = StrOutputParser()
        return prompt | self._model | parser

    async def execute(self, state: State) -> dict:
        task = state["task"]
        chain = self._create_chain()
        comments = await chain.ainvoke({
            "subdivision": task.subdivision,
            "description": task.description,
            "hours": task.hours
        })
        return {"comments": comments}
