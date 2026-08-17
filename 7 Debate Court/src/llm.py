import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
try:
    import json_repair
except ImportError:
    json_repair = None
from config import (
    MAX_JSON_RETRIES,
    NUM_CTX,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

def get_llm(temperature: float, num_predict: int = 512) -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        num_ctx=NUM_CTX,
        num_predict=num_predict,
    )

def _extract_json(text: str) -> dict:
    """Pull the first {...} JSON object out of a model response, stripping
    markdown code fences if the model wrapped its answer in them.

    Handles two common small-model failure modes:
    - malformed-but-complete JSON (missing comma, stray quote, etc.)
    - truncated JSON (generation hit num_predict before closing braces),
      which has no matching closing '}' at all.
    """
    cleaned = text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned.strip(), flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned.strip()).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            if json_repair is not None:
                repaired = json_repair.loads(json_str)
                if isinstance(repaired, dict) and repaired:
                    return repaired
    start = cleaned.find("{")
    if start != -1 and json_repair is not None:
        candidate = cleaned[start:]
        repaired = json_repair.loads(candidate)
        if isinstance(repaired, dict) and repaired:
            return repaired
        
    raise ValueError(f"No JSON object found in model output:\n{text[:500]}")

def call_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    num_predict: int = 700,
    max_retries: int = MAX_JSON_RETRIES,
) -> dict:
    """Call the model and force-parse a JSON object out of its reply,
    retrying with corrective feedback if parsing fails."""
    llm = get_llm(temperature=temperature, num_predict=num_predict)
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

    last_error = None
    for _ in range(max_retries):
        response = llm.invoke(messages)
        raw = response.content
        try:
            return _extract_json(raw)
        except Exception as exc:
            last_error = exc
            messages.append(response)
            messages.append(
                HumanMessage(
                    content=(
                        "That response was not valid JSON. "
                        f"Error: {exc}. Reply again with ONLY a single valid JSON "
                        "object matching the schema. No markdown fences, no commentary "
                        "before or after it."
                    )
                )
            )

    raise RuntimeError(
        f"Failed to get valid JSON from '{OLLAMA_MODEL}' after {max_retries} attempts: "
        f"{last_error}"
    )

def call_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    num_predict: int = 500,
) -> str:
    llm = get_llm(temperature=temperature, num_predict=num_predict)
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)
    return response.content.strip()