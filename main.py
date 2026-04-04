import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend
from fastapi_cache.decorator import cache
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from memcache import Memcache
from pydantic import BaseModel, Field, NonNegativeFloat, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    memcached = Memcache(("memcached", 11211))
    FastAPICache.init(MemcachedBackend(memcached), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

SYSTEM_PROMPT = """\
Ты — ассистент-редактор заданий для сотрудников.
Твоя задача — оценивать задания по пяти ключевым критериям и предоставлять развернутую обратную связь.

Критерии оценки (по 20-балльной шкале, суммарно 100 баллов):
1. Формат (20 баллов) - соответствие стандартному шаблону
2. Полнота (20 баллов) - наличие всех реквизитов (тикет, ФИО, контрагент)
3. Конкретность (25 баллов) - измеримость и детализация действий
4. Время (20 баллов) - адекватность часов выполнения
5. Соответствие (15 баллов) - логичность для подразделения

Шкала перевода в 10-балльную систему:
90-100 баллов → 10 (идеально)
80-89 → 9 (отлично)
70-79 → 8 (хорошо)
60-69 → 7 (удовлетворительно)
50-59 → 6 (недостатки)
40-49 → 5 (плохо)
<40 → 1-4 (критично)

Обязательные элементы вывода:
1. Итоговый балл (1-10)
2. Сводка по критериям (сырые баллы)
3. Сильные стороны
4. Конкретные рекомендации
5. Критические проблемы (если есть)

Пример правильного задания:
Контрагент: КЕЖУЙ НЕФТЕГАЗОВЫЕ УСЛУГИ ООО  
Подразделение: Отдел автоматизации ЗУП  
Описание:  
- Тикет №КЖ000000119  
- Инициатор: Калачева Г.Ю.  
- Запрос: верификация расчета резерва на отпуска  
Работы:  
1. Проверить процент исчисления резерва  
2. Сверить лимит суммы резерва  
3. Протестировать алгоритм расчета в системе  
Часы: 3  

Пример плохого задания:
Контрагент: БСТ ООО  
Подразделение: Отдел автоматизации БУ и УУ  
Описание: "Метрополитен"  
Работы: Создана инструкция по Оценочным обязательствам  
Часы: 100
"""

PROMPT_TEMPLATE = """\
Проанализируй текущее задание:
Тема: {theme}  
Подразделение: {subdivision}  
Описание: {description}  
Часы: {hours}  
Работы: {jobs}  """


class YandexCloudSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="YANDEX_CLOUD_")

    api_key: str = "<API_KEY>"
    folder_id: str = "<FOLDER_ID>"
    base_url: str = "https://llm.api.cloud.yandex.net/v1"

    @property
    def aliceai_llm(self) -> str:
        return f"gpt://{self.folder_id}/aliceai-llm"

    @property
    def yandexgpt_rc(self) -> str:
        return f"gpt://{self.folder_id}/yandexgpt/rc"


settings = YandexCloudSettings()

model = ChatOpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
    model=settings.aliceai_llm,
    temperature=0.2,
)


class Job(BaseModel):
    hours: NonNegativeFloat
    content: str | None = None

    def to_text(self, index: int) -> str:
        return f"""\
        {index}. **Количество часов**: {self.hours}; **Содержание**: {self.content}
        """


class Task(BaseModel):
    subdivision: str
    theme: str
    description: str | None = None
    hours: float
    jobs: list[Job] | None = None


class TaskReview(BaseModel):
    """Проверенное задание сотруднику"""

    rate: PositiveInt = Field(ge=1, le=10, description="Итоговая оценка от 1 до 10")
    comments: str = Field(description="Комментарии и рекомендации по улучшению")


agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    response_format=ToolStrategy(TaskReview),
)


@app.post(
    path="/api/v1/tasks/",
    status_code=status.HTTP_200_OK,
    response_model=TaskReview,
)
@cache(expire=3600)
async def review_task(task: Task) -> TaskReview:
    result = await agent.ainvoke({
        "messages": [("human", PROMPT_TEMPLATE.format(
            subdivision=task.subdivision,
            theme=task.theme,
            description=task.description,
            hours=task.hours,
            jobs="\n\n".join([job.to_text(i + 1) for i, job in enumerate(task.jobs)]),
        ))]
    })
    return result["structured_response"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
