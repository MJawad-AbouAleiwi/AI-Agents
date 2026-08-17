# Builds the LangGraph StateGraph
from langgraph.graph import END, StateGraph
from nodes import advocate_node, final_verdict_node, judge_node, opponent_node
from state import DebateState

def route_after_judge(state: DebateState) -> str:
    return "rebuttal" if state.get("continue_debate") else "final"

def build_graph():
    graph = StateGraph(DebateState)

    graph.add_node("advocate", advocate_node)
    graph.add_node("opponent", opponent_node)
    graph.add_node("judge", judge_node)
    graph.add_node("final_verdict", final_verdict_node)

    graph.set_entry_point("advocate")
    graph.add_edge("advocate", "opponent")
    graph.add_edge("opponent", "judge")
    graph.add_conditional_edges(
        "judge",
        route_after_judge,
        {"rebuttal": "advocate", "final": "final_verdict"},
    )
    graph.add_edge("final_verdict", END)

    return graph.compile()