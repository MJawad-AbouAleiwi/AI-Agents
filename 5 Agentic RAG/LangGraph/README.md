# Agentic RAG (LangGraph)

Paul is a small AI agent who acts like a butler at a gala. He can:

- Look up gala guests from a list,
- Search the web for general knowledge,
- Check the weather,
- Look up the most popular AI models on the Hugging Face Hub.

## How it works (big picture)

LangGraph makes you draw the agent's control flow explicitly as a graph.

```
START --> assistant --> (needs a tool?) --> tools --> assistant --> ... --> END
```

This loop repeats (assistant → tools → assistant → ...) until the model
gives a final answer with no more tool calls needed.

1. **Retrieval**: `retriever.py` downloads a small guest-list dataset and
   builds a BM25 keyword-search index over it.
2. **Tools**: `tools.py` defines three more tools - web search, weather
   lookup, and Hugging Face Hub model stats.
3. **Agent**: `app.py` wires a local language model together with all
   four tools into a compiled LangGraph graph called Paul.

## Project Structure

```
paul_langgraph/
├── retriever.py      # Loads guest data + builds the guest search tool
├── tools.py           # Web search, weather, and Hugging Face Hub stats tools
├── app.py             # Builds Paul's graph and runs 4 example questions
├── requirements.txt   # Python dependencies
```

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure Ollama is running with llama3.2 pulled**

   ```bash
   ollama pull llama3.2   # only needed once
   ollama serve           # usually starts automatically on desktop installs
   ```

3. **Run Paul**

   ```bash
   python app.py
   ```
   This will run 4 example conversations and print Paul's answers to the terminal.