import logging
import asyncio
from pprint import pprint

from langchain_gigachat import GigaChat

from src.ai_agent.agent import Agent
from src.ai_agent.nodes import RateNode, CommentsNode
from src.models import Task
from src.settings import settings


giga_chat = GigaChat(
    credentials=settings.giga_chat.api_key,
    scope=settings.giga_chat.scope,
    verify_ssl_certs=False,
    profanity_check=False,
    # temperature=0.2
)


agent = Agent(RateNode(giga_chat), CommentsNode(giga_chat))


task = Task(
    partner="АЛЬКОР ЗАО МПКФ",
    subdivision="Отдел автоматизации БУ и УУ",
    description="""Метрополитен""",
    hours=100
)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    res = await agent.generate(task)
    pprint(res)


asyncio.run(main())
