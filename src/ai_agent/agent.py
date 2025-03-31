from langgraph.graph import START, END, StateGraph

from src.core.entities import Task
from src.ai_agent.state import State
from src.ai_agent.nodes import RateNode, CommentsNode


class Agent:
    def __init__(
            self,
            rate_node: RateNode,
            comments_node: CommentsNode
    ) -> None:
        graph = StateGraph(State)

        graph.add_node("rates", rate_node)
        graph.add_node("comment", comments_node)

        graph.add_edge(START, "rates")
        graph.add_edge("rates", "comment")
        graph.add_edge("comment", END)

        self._graph_compiled = graph.compile()

    async def generate(self, task: Task) -> dict:
        return await self._graph_compiled.ainvoke({"task": task})
