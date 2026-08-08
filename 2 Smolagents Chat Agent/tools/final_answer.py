# Defines the FinalAnswerTool, which the agent must call to return its final answer to the user.

from smolagents.tools import Tool

class FinalAnswerTool(Tool):
    # The name the agent will use to call this tool.
    name = "final_answer"

    # Description shown to the LLM so it knows when to use this tool.
    description = "Provides a final answer to the given problem."

    # Expected input schema.
    inputs = {
        "answer": {
            "type": "any",
            "description": "The final answer to the problem",
        }
    }

    # The tool can return any type.
    output_type = "any"

    def forward(self, answer: any) -> any:
        # Simply pass the answer straight through.
        return answer

    def __init__(self, *args, **kwargs):
        self.is_initialized = False