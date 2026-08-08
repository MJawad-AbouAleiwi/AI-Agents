# Entry point for a smolagents-powered AI agent with a Gradio chat UI.
# The agent can reason and write/execute Python code to answer questions. 
# It is backed by a Hugging Face Inference API model and exposes a small set of custom tools.

from smolagents import CodeAgent, InferenceClientModel, load_tool, tool
from tools.final_answer import FinalAnswerTool
from smolagents import GradioUI
import datetime
import requests
import pytz
import yaml

# Tools are plain Python functions decorated with @tool. 
# smolagents uses docstring to tell the LLM what the tool does and what arguments it expects.
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet - replace this with something useful!

    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.

    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Look up the timezone object
        tz = pytz.timezone(timezone)
        # Format the current time in that timezone as a readable string
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        # Return a friendly error message instead of raising, so the agent
        # can see what went wrong and try again.
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

@tool
def get_city_coordinates(city: str, country: str) -> str:
    """Returns the geographic coordinates of a city.

    Args:
        city: The name of the city, such as 'Beirut' or 'Paris'.
        country: The country where the city is located, such as 'Lebanon' or 'France'.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "city": city,
            "country": country,
            "format": "json",
            "limit": 1,
        }

        headers = {
            "User-Agent": "smolagents-city-agent/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return f"Could not find {city}, {country}."

        location = data[0]

        latitude = location.get("lat")
        longitude = location.get("lon")
        display_name = location.get("display_name", f"{city}, {country}")

        return (
            f"Location: {display_name}\n"
            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}"
        )

    except requests.exceptions.RequestException as e:
        return f"Error finding {city}, {country}: {str(e)}"

    except Exception as e:
        return f"Error processing location: {str(e)}"

# This is how the agent formally returns its final response.
final_answer = FinalAnswerTool()

# Example of loading a ready-made tool from the Hugging Face Hub.
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# InferenceClientModel talks to the Hugging Face Inference API to run the LLM that powers the agent's reasoning.
model = InferenceClientModel(
    max_tokens=2096,       # Max tokens generated per model call
    temperature=0.5,       # Randomness of generations (0 = deterministic, 1 = creative)
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

# CodeAgent can write and execute Python code as part of its reasoning loop.
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone, get_city_coordinates, image_generation_tool],
    max_steps=6,        # Max reasoning/action steps before giving up
    verbosity_level=1,  # Logging verbosity (0 = quiet, higher = more detail)
    planning_interval=None, # Set an int to make the agent re-plan every N steps
    name=None,
    description=None
)

# Launch the Gradio web chat interface for the agent.
if __name__ == "__main__":
    GradioUI(agent).launch()