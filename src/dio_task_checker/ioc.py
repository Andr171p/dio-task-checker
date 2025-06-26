from dishka import Provider, provide, Scope, from_context, make_async_container

from langchain_core.runnables import Runnable
from langchain_core.language_models import BaseChatModel

from langchain_gigachat import GigaChat

from .agent import create_structured_output_llm_chain
from .schemas import CheckedTask
from .prompts import TEMPLATE
from .settings import GigaChatSettings


class AppProvider(Provider):
    config = from_context(provides=GigaChatSettings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_model(self, config: GigaChatSettings) -> BaseChatModel:
        return GigaChat(
            credentials=config.API_KEY,
            scope=config.SCOPE,
            model=config.MODEL,
            verify_ssl_certs=False,
            profanity_check=False
        )

    @provide(scope=Scope.APP)
    def get_agent(self, model: BaseChatModel) -> Runnable:
        return create_structured_output_llm_chain(
            schema=CheckedTask,
            template=TEMPLATE,
            model=model
        )


settings = GigaChatSettings()

container = make_async_container(AppProvider(), context={GigaChatSettings: settings})
