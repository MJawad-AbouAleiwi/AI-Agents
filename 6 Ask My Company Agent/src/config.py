import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Models
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:latest")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Generation settings
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "120.0"))
CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", "3072"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "64"))
SIMILARITY_TOP_K = int(os.getenv("SIMILARITY_TOP_K", "3"))

# Paths
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_PROJECT_ROOT, "data")
STORAGE_DIR = os.path.join(_PROJECT_ROOT, "storage")