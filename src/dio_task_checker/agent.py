from typing import Type

from pydantic import BaseModel

from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser


def create_structured_output_llm_chain(
        schema: Type[BaseModel],
        template: str,
        model: BaseChatModel
) -> Runnable:
    parser = PydanticOutputParser(pydantic_object=schema)
    return (
        ChatPromptTemplate
        .from_messages([("system", template)])
        .partial(format_instructions=parser.get_format_instructions())
        | model
        | parser
    )
