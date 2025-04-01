from dishka import Provider, provide, Scope

from langchain_core.language_models import BaseChatModel, LLM
from langchain_gigachat import GigaChat

from src.ai_agent.agent import Agent
from src.ai_agent.nodes import RateNode, CommentsNode
from src.task_assistant import TaskAssistant

from src.settings import settings


class TaskAssistantProvider(Provider):
    @provide(scope=Scope.APP)
    def get_llm(self) -> BaseChatModel | LLM:
        return GigaChat(
            credentials=settings.giga_chat.api_key,
            scope=settings.giga_chat.scope,
            verify_ssl_certs=False,
            profanity_check=False
        )

    @provide(scope=Scope.APP)
    def get_rate_node(self, model: BaseChatModel | LLM) -> RateNode:
        return RateNode(model)

    @provide(scope=Scope.APP)
    def get_comments_node(self, model: BaseChatModel | LLM) -> CommentsNode:
        return CommentsNode(model)

    @provide(scope=Scope.APP)
    def get_agent(self, rate_node: RateNode, comments_node: CommentsNode) -> Agent:
        return Agent(rate_node, comments_node)

    @provide(scope=Scope.APP)
    def get_task_assistant(self, agent: Agent) -> TaskAssistant:
        return TaskAssistant(agent)
