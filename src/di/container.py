from dishka import make_async_container

from src.di.provider import TaskAssistantProvider


container = make_async_container(TaskAssistantProvider())
