from langgraph.graph.graph import CompiledGraph
from langgraph.graph import START, END, StateGraph

from .state import AgentState
from .nodes import CommentNode, RateNode


def create_task_checker_agent(comment: CommentNode, rate: RateNode) -> CompiledGraph:
    workflow = (
        StateGraph(AgentState)
        .add_node("comment", comment)
        .add_node("rate", rate)
        .add_edge(START, "rate")
        .add_edge("rate", "comment")
        .add_edge("comment", END)
    )
    return workflow.compile()
