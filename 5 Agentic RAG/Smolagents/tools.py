# This file holds Paul's extra tools, besides guest lookup.
import random
from huggingface_hub import list_models
from smolagents import Tool

class WeatherInfoTool(Tool):
    """
    Returns dummy weather data for a given location.
    """
    name = "weather_info"
    description = "Fetches dummy weather information for a given location."
    inputs = {
        "location": {
            "type": "string",
            "description": "The location to get weather information for.",
        }
    }
    output_type = "string"

    def forward(self, location: str) -> str:
        # A small set of weather conditions we pick from at random
        weather_conditions = [
            {"condition": "Rainy", "temp_c": 15},
            {"condition": "Clear", "temp_c": 25},
            {"condition": "Windy", "temp_c": 20},
        ]
        data = random.choice(weather_conditions)
        return f"Weather in {location}: {data['condition']}, {data['temp_c']}°C"

class HubStatsTool(Tool):
    """
    Looks up the most-downloaded model by a given author/organization
    on the Hugging Face Hub (e.g. "facebook", "google", "openai-community").
    """
    name = "hub_stats"
    description = "Fetches the most downloaded model from a specific author on the Hugging Face Hub."
    inputs = {
        "author": {
            "type": "string",
            "description": "The username of the model author/organization to find models from.",
        }
    }
    output_type = "string"

    def forward(self, author: str) -> str:
        try:
            # Ask the Hugging Face Hub for that author's models.
            models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))
            if models:
                model = models[0]
                return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
            return f"No models found for author {author}."
        except Exception as e:
            # Never let the agent crash because of a network/ API error.
            return f"Error fetching models for {author}: {str(e)}"