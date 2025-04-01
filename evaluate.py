import logging
import asyncio

import numpy as np
import pandas as pd

from langchain_gigachat import GigaChat

from src.models import Task
from src.ai_agent.agent import Agent
from src.task_assistant import TaskAssistant
from src.ai_agent.nodes import RateNode, CommentsNode

from src.settings import settings


logging.basicConfig(level=logging.INFO)


model = GigaChat(
    credentials=settings.giga_chat.api_key,
    scope=settings.giga_chat.scope,
    verify_ssl_certs=False,
    profanity_check=False
)

rate_node = RateNode(model)

comments_node = CommentsNode(model)

agent = Agent(rate_node, comments_node)

task_assistant = TaskAssistant(agent)


df = pd.read_excel("задания февраль.xls")


async def main() -> pd.DataFrame:
    results = []
    for _, row in df.iterrows():
        try:
            task = Task(
                partner=row["Контрагент"],
                subdivision=row["Подразделение"],
                description=row["Описание"] if row["Описание"] is not np.nan else "",
                hours=row["Часы"]
            )
            checked_task = await task_assistant.check_task(task)
            result = {
                "Номер": row["Номер"],
                "Контрагент": task.partner,
                "Подразделение": task.subdivision,
                "Описание": task.description,
                "Часы": task.hours,
                "Оценка": checked_task.rate,
                "Комментарии": checked_task.comments
            }
            results.append(result)
        except Exception as ex:
            logging.error(ex)
    result_df = pd.DataFrame(results)
    result_df.to_csv("evaluated_tasks.csv")
    return result_df


if __name__ == "__main__":
    asyncio.run(main())
