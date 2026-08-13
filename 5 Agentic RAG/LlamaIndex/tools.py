# This file holds Paul's extra tools, besides guest lookup.
import random
from huggingface_hub import list_models
from llama_index.core.tools import FunctionTool
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec

# Web search tool (DuckDuckGo)
_duckduckgo_spec = DuckDuckGoSearchToolSpec()
search_tool = FunctionTool.from_defaults(_duckduckgo_spec.duckduckgo_full_search)

# Weather tool
# ---------------------------------------------------------------------------
def get_weather_info(location: str) -> str:
    """Fetches dummy weather information for a given location."""
    # A small set of weather conditions we pick from at random
    weather_conditions = [
        {"condition": "Rainy", "temp_c": 15},
        {"condition": "Clear", "temp_c": 25},
        {"condition": "Windy", "temp_c": 20},
    ]
    data = random.choice(weather_conditions)
    return f"Weather in {location}: {data['condition']}, {data['temp_c']}°C"

weather_info_tool = FunctionTool.from_defaults(get_weather_info)

# Hugging Face Hub stats tool
def get_hub_stats(author: str) -> str:
    """Fetches the most downloaded model from a specific author on the Hugging Face Hub."""
    try:
        # Ask the Hugging Face Hub for that author's models.
        models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))
        if models:
            model = models[0]
            return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
        return f"No models found for author {author}."
    except Exception as e:
        # Never let the agent crash because of a network/API error.
        return f"Error fetching models for {author}: {str(e)}"

hub_stats_tool = FunctionTool.from_defaults(get_hub_stats)