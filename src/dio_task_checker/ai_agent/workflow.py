from langgraph.graph.graph import CompiledGraph
from langgraph.graph import START, END, StateGraph

from .state import AgentState
from .nodes import CommentNode, EvaluateNode


def create_task_checker_agent(comment: CommentNode, evaluate: EvaluateNode) -> CompiledGraph:
    workflow = (
        StateGraph(AgentState)
        .add_node("comment", comment)
        .add_node("evaluate", evaluate)
        .add_edge(START, "evaluate")
        .add_edge("evaluate", "comment")
        .add_edge("comment", END)
    )
    return workflow.compile()
