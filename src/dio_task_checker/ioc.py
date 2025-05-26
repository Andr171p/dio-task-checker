from dishka import Provider, provide, Scope, from_context, make_async_container

from langchain_core.language_models import BaseChatModel

from langchain_gigachat import GigaChat

from langgraph.graph.graph import CompiledGraph

from .settings import GigaChatSettings
from .ai_agent.nodes import CommentNode, RateNode
from .ai_agent.workflow import create_task_checker_agent


class AppProvider(Provider):
    config = from_context(provides=GigaChatSettings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_model(self, config: GigaChatSettings) -> BaseChatModel:
        return GigaChat(
            credentials=config.API_KEY,
            scope=config.SCOPE,
            verify_ssl_certs=False,
            profanity_check=False
        )

    @provide(scope=Scope.APP)
    def get_comment_node(self, model: BaseChatModel) -> CommentNode:
        return CommentNode(model)

    @provide(scope=Scope.APP)
    def get_rate_node(self, model: BaseChatModel) -> RateNode:
        return RateNode(model)

    @provide(scope=Scope.APP)
    def get_agent(self, comment: CommentNode, rate: RateNode) -> CompiledGraph:
        return create_task_checker_agent(comment, rate)


settings = GigaChatSettings()

container = make_async_container(AppProvider(), context={GigaChatSettings: settings})
