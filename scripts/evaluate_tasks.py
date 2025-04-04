import logging
import asyncio

import pandas as pd

from langchain_gigachat import GigaChat

from src.models import Task, Job
from src.ai_agent import TaskAIAgent
from src.task_assistant import TaskAssistant
from src.ai_agent.nodes import RateNode, CommentsNode

from src.settings import settings, BASE_DIR


logging.basicConfig(level=logging.INFO)


model = GigaChat(
    credentials=settings.giga_chat.api_key,
    scope=settings.giga_chat.scope,
    verify_ssl_certs=False,
    profanity_check=False
)

rate_node = RateNode(model)

comments_node = CommentsNode(model)

ai_agent = TaskAIAgent(rate_node, comments_node)

task_assistant = TaskAssistant(ai_agent)


RAW_DATA_DIR = BASE_DIR / "raw_data"

TASKS_PATH = RAW_DATA_DIR / "задания февраль + темы.xls"

JOBS_PATH = RAW_DATA_DIR / "задания февраль работы.xls"


tasks_df = pd.read_excel(TASKS_PATH)

jobs_df = pd.read_excel(JOBS_PATH)

tasks_df = tasks_df.drop(tasks_df.index[:2])
jobs_df = jobs_df.drop(jobs_df.index[:1])
tasks_columns = ["Дата", "Номер", "Контрагент", "Подразделение", "Тема", "Описание", "Часы"]
jobs_columns = ["Дата", "Номер", "НомерСтроки", "КоличествоЧасов", "Содержание"]
tasks_df.columns = tasks_columns
jobs_df.columns = jobs_columns


def get_jobs_by_task_number(task_number: str) -> pd.DataFrame:
    return jobs_df[jobs_df["Номер"] == task_number]


async def main() -> None:
    results = []
    for _, row in tasks_df.iterrows():
        try:
            jobs = get_jobs_by_task_number(row["Номер"])
            task = Task(
                theme=row["Тема"],
                subdivision=row["Подразделение"],
                description=row["Описание"],
                hours=row["Часы"],
                jobs=[Job(hours=job["КоличествоЧасов"], content=job["Содержание"]) for _, job in jobs.iterrows()]
            )
            checked_task = await task_assistant.check_task(task)
            result = {
                "Номер": row["Номер"],
                "Контрагент": row["Контрагент"],
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
    result_df.to_csv("evaluated_tasks_with_jobs.csv")
    
    
if __name__ == "__main__":
    asyncio.run(main())
