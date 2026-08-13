# This is the entry point. Run this file to bring Paul to life and watch him answer a few example questions.
import warnings
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel
from retriever import build_guest_info_tool
from tools import HubStatsTool, WeatherInfoTool
warnings.filterwarnings("ignore")

def build_paul() -> CodeAgent:
    """
    Assemble Paul: one language model + four tools.

    Returns:
        CodeAgent: the ready-to-use agent.
    """
    # The brain of the agent
    model = LiteLLMModel(model_id="ollama/llama3.2", api_base="http://localhost:11434")
    # Build each tool
    guest_info_tool = build_guest_info_tool()   # Searches the guest list
    search_tool = DuckDuckGoSearchTool()         # Searches the web
    weather_info_tool = WeatherInfoTool()        # Dummy weather lookup
    hub_stats_tool = HubStatsTool()              # Hugging Face Hub model stats

    # Combine everything into one agent
    paul = CodeAgent(
        tools=[guest_info_tool, search_tool, weather_info_tool, hub_stats_tool],
        model=model,
    )
    return paul

def ask(agent: CodeAgent, title: str, question: str) -> None:
    """Small helper to run one example query and print it nicely."""
    print("=" * 80)
    print(title)
    print("-" * 80)
    print(f"Question: {question}\n")
    response = agent.run(question)
    print(f"Paul's Response:\n{response}\n")

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
    ask(
        paul,
        "Example 4: Combining Multiple Tools",
        "What is Facebook and what's their most popular model on the Hugging Face Hub?",
    )

if __name__ == "__main__":
    main()