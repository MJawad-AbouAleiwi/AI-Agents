import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from src import config

def configure_settings() -> None:
    """Point LlamaIndex's global Settings at our local Ollama models."""
    Settings.llm = Ollama(
        model=config.LLM_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        request_timeout=config.REQUEST_TIMEOUT,
        temperature=config.LLM_TEMPERATURE,
        context_window=config.CONTEXT_WINDOW,
    )
    Settings.embed_model = OllamaEmbedding(
        model_name=config.EMBED_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )
    Settings.node_parser = SentenceSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

def build_index(force_rebuild: bool = False) -> VectorStoreIndex:
    configure_settings()

    docstore_path = os.path.join(config.STORAGE_DIR, "docstore.json")
    if os.path.exists(docstore_path) and not force_rebuild:
        print(f"Loading existing index from {config.STORAGE_DIR} ...")
        storage_context = StorageContext.from_defaults(persist_dir=config.STORAGE_DIR)
        return load_index_from_storage(storage_context)

    print(f"Reading documents from {config.DATA_DIR} ...")
    documents = SimpleDirectoryReader(
        input_dir=config.DATA_DIR,
        recursive=True,
        filename_as_id=True,
    ).load_data()

    if not documents:
        raise RuntimeError(
            f"No documents found under {config.DATA_DIR}. Add policy/procedure "
            "files under data/company_policies/ and data/procedures/, then re-run."
        )

    # Tag each document with its top-level folder
    for doc in documents:
        file_path = doc.metadata.get("file_path", "")
        rel_path = os.path.relpath(file_path, config.DATA_DIR) if file_path else ""
        doc.metadata["category"] = rel_path.split(os.sep)[0] if rel_path else "unknown"

    print(f"Indexing {len(documents)} document(s) — this embeds every chunk locally...")
    index = VectorStoreIndex.from_documents(documents, show_progress=True)

    os.makedirs(config.STORAGE_DIR, exist_ok=True)
    index.storage_context.persist(persist_dir=config.STORAGE_DIR)
    print(f"Index persisted to {config.STORAGE_DIR}")
    return index

if __name__ == "__main__":
    rebuild = "--rebuild" in sys.argv
    build_index(force_rebuild=rebuild)
    print("Done. Run `python -m src.main` to start chatting.")