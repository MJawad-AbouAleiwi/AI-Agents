# This is the entry point. Run this file to bring Paul to life and watch him answer a few example questions.
import warnings
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from retriever import build_guest_info_tool
from tools import hub_stats_tool, search_tool, weather_info_tool
warnings.filterwarnings("ignore")

class AgentState(TypedDict):
    """
    The "memory" that flows through the graph: just a growing list of
    chat messages (human, AI, and tool-result messages). `add_messages`
    tells LangGraph to append new messages instead of overwriting the list.
    """
    messages: Annotated[list[AnyMessage], add_messages]

def build_paul():
    """
    Assemble Paul: one local language model + four tools, wired into a
    small LangGraph state graph.

    Returns:
        A compiled LangGraph graph, ready to `.invoke(...)`.
    """
    # The "brain" of the agent.
    llm = ChatOllama(model="llama3.2", temperature=0)

    # Build the guest lookup tool and collect all four tools together
    guest_info_tool = build_guest_info_tool()
    tools = [guest_info_tool, search_tool, weather_info_tool, hub_stats_tool]

    # bind_tools tells the model which tools it's allowed to call.
    chat_with_tools = llm.bind_tools(tools)

    def assistant(state: AgentState):
        """The 'assistant' node: ask the model what to do next."""
        return {"messages": [chat_with_tools.invoke(state["messages"])]}

    # Build the graph
    builder = StateGraph(AgentState)

    # Nodes: these do the work
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    # Edges: these determine how control flows between nodes
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        # If the model's last message requested a tool call, go run it.
        # Otherwise, the graph ends and we return the model's answer.
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    return builder.compile()

def ask(paul, title: str, question: str) -> None:
    """
    Small helper to run one example query and print it nicely.

    Wrapped in a try/except so that if ONE example fails (network issue,
    Ollama not running, etc.), the script keeps going and still runs the
    remaining examples instead of crashing entirely.
    """
    print("=" * 80)
    print(title)
    print("-" * 80)
    print(f"Question: {question}\n")
    messages = [HumanMessage(content=question)]
    response = paul.invoke({"messages": messages})
    print(f"Paul's Response:\n{response['messages'][-1].content}\n")

def main():
    paul = build_paul()
    # Example 1: Finding Guest Information
    ask(
        paul,
        "Example 1: Finding Guest Information",
        "Tell me about our guest named 'Lady Ada Lovelace'.",
    )
    # Example 2: Checking the Weather for Fireworks
    ask(
        paul,
        "Example 2: Checking the Weather for Fireworks",
        "What's the weather like in Paris tonight? Will it be good for fireworks?",
    )
    # Example 3: Impressing AI Researchers
    ask(
        paul,
        "Example 3: Impressing AI Researchers",
        "One of our guests is a researcher from Facebook (Meta). "
        "What is their most downloaded model on the Hugging Face Hub, "
        "and can you say something impressive about it?",
    )
    # Example 4: Combining Multiple Tools
    ask(
        paul,
        "Example 4: Combining Multiple Tools",
        "What is Facebook and what's their most popular model on the Hugging Face Hub?",
    )

if __name__ == "__main__":
    main()