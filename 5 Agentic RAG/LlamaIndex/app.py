# This is the entry point. Run this file to bring Paul to life and watch him answer a few example questions.
import asyncio
import warnings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from retriever import build_guest_info_tool
from tools import hub_stats_tool, search_tool, weather_info_tool
warnings.filterwarnings("ignore")

def build_paul() -> AgentWorkflow:
    """
    Assemble Paul: one local language model + four tools.

    Returns:
        AgentWorkflow: the ready-to-use agent.
    """
    # The brain of the agent
    llm = Ollama(model="llama3.2", request_timeout=120.0)

    # Build each tool
    guest_info_tool = build_guest_info_tool()
    # Combine everything into one agent
    paul = AgentWorkflow.from_tools_or_functions(
        [guest_info_tool, search_tool, weather_info_tool, hub_stats_tool],
        llm=llm,
    )
    return paul

async def ask(agent: AgentWorkflow, title: str, question: str) -> None:
    """
    Small helper to run one example query and print it nicely.
    """
    print("=" * 80)
    print(title)
    print("-" * 80)
    print(f"Question: {question}\n")
    response = await agent.run(question)
    print(f"Paul's Response:\n{response}\n")

async def main():
    paul = build_paul()
    # Example 1: Finding Guest Information
    await ask(
        paul,
        "Example 1: Finding Guest Information",
        "Tell me about our guest named 'Lady Ada Lovelace'.",
    )
    # Example 2: Checking the Weather for Fireworks
    await ask(
        paul,
        "Example 2: Checking the Weather for Fireworks",
        "What's the weather like in Paris tonight? Will it be good for fireworks?",
    )
    # Example 3: Impressing AI Researchers
    await ask(
        paul,
        "Example 3: Impressing AI Researchers",
        "One of our guests is a researcher from Facebook (Meta). "
        "What is their most downloaded model on the Hugging Face Hub, "
        "and can you say something impressive about it?",
    )
    # Example 4: Combining Multiple Tools
    await ask(
        paul,
        "Example 4: Combining Multiple Tools",
        "What is Facebook and what's their most popular model on the Hugging Face Hub?",
    )

if __name__ == "__main__":
    asyncio.run(main())