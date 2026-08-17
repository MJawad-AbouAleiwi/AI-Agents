import os
# Model
OLLAMA_MODEL = os.getenv("DEBATE_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Memory
NUM_CTX = int(os.getenv("DEBATE_NUM_CTX", "4096"))
NUM_PREDICT_ARGUMENT = int(os.getenv("DEBATE_NUM_PREDICT_ARGUMENT", "450"))
NUM_PREDICT_JUDGE = int(os.getenv("DEBATE_NUM_PREDICT_JUDGE", "1000"))
NUM_PREDICT_FINAL = int(os.getenv("DEBATE_NUM_PREDICT_FINAL", "1000"))
TEMPERATURE_DEBATER = float(os.getenv("DEBATE_TEMP_DEBATER", "0.7"))
TEMPERATURE_JUDGE = float(os.getenv("DEBATE_TEMP_JUDGE", "0.2"))

# Debate structure
MAX_ROUNDS_DEFAULT = int(os.getenv("DEBATE_MAX_ROUNDS", "3"))
MAX_JSON_RETRIES = int(os.getenv("DEBATE_JSON_RETRIES", "3"))
HISTORY_WINDOW = int(os.getenv("DEBATE_HISTORY_WINDOW", "1"))