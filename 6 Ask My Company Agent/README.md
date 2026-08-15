# Ask My Company - Internal Policy Agent

A local agentic RAG assistant that answers employee questions by searching the actual company policy documents.

## How it Works

- **LLM**: `llama3.2` via Ollama.
- **Embeddings**: `nomic-embed-text` via Ollama.
- **Orchestration**: [LlamaIndex](https://docs.llamaindex.ai).
- **Agent**: decides when to search the docs, can list what's indexed, and is instructed to never answer from general knowledge.

## 1. Install Python Dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Build the Index

```bash
python -m src.ingest
```

This reads every file under `data/`, splits it into chunks, embeds each
chunk with `nomic-embed-text`, and persists the vector index to `storage/`.

## 3. Chat with the Agent

```bash
python -m src.main
```

```
You: How many vacation days do I get after 4 years?
Agent: Employees with 3–5 years of tenure accrue 20 vacation days per year...

You: Can I work remotely from another country?
Agent: Domestic remote work is generally approved, but working from another
country requires prior approval from HR and Legal due to tax and visa
implications, and is capped at 30 consecutive days without special approval...
```

## Project layout

```
ask-my-company-agent/
├── data/
│   ├── company_policies/   # Vacation, expenses, remote_work, sick_leave...
│   └── procedures/         # Onboarding, purchasing, IT_support...
├── storage/                 # Persisted vector index
├── src/
│   ├── config.py            # All tunable settings live here
│   ├── ingest.py            # Builds the vector index
│   ├── agent.py             # Agent and tools
│   └── main.py              # CLI chat loop
├── requirements.txt
```