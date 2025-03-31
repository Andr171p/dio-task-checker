import logging
import asyncio
from pprint import pprint

from langchain_gigachat import GigaChat

from src.ai_agent.agent import Agent
from src.ai_agent.nodes import RateNode, CommentsNode
from src.core.entities import Task
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
    subdivision="Отдел автоматизации ЗУП",
    description="""Инициатор: Валова Ирина Владимировна (8-922-267-66-37)
                    Задание:
                    1. Как вывести всех сотрудников у которых есть трудовые книжки
                    2. Почему у Дмитриченко ДВ, Фахрутдинова, Слободчикова СН, Слободчикова АН не отражаются данные в СТД-Р по трудовым книжкам.""",
    hours=0.75
)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    res = await agent.generate(task)
    pprint(res)


asyncio.run(main())
