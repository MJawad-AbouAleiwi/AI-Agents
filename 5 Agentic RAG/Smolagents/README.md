# Agentic RAG (smolagents)

Paul is a small AI agent who acts like a butler at a gala. He can:

- Look up gala guests from a list,
- Search the web for general knowledge,
- Check the weather,
- Look up the most popular AI models on the Hugging Face Hub.

## How it Works

1. **Retrieval**: `retriever.py` downloads a small guest-list dataset and
   builds a keyword-search index over it.
2. **Tools**: `tools.py` defines two extra tools - weather lookup and
   Hugging Face Hub model stats.
3. **Agent**: `app.py` wires a language model together with all four tools
   into one `CodeAgent` called Paul.

## Project Structure

```
Smolagents/
├── retriever.py      # Loads guest data + builds the guest search tool
├── tools.py           # Weather tool + Hugging Face Hub stats tool
├── app.py             # Builds Paul and runs 4 example questions
├── requirements.txt   # Python dependencies
```

## Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Hugging Face Token**

   ```bash
   $env:HF_TOKEN="your_hugging_face_token_here"
   ```

3. **Run Paul**

   ```bash
   python app.py
   ```

   This will run 4 example conversations and print Paul's answers to the terminal.