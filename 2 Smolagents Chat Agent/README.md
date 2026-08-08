# Smolagents Chat Agent

An AI agent built with [smolagents](https://github.com/huggingface/smolagents), served through a Gradio chat UI. 

The agent can reason and write/execute Python code to answer questions,
and comes with a couple of example tools you can extend.

## Files

- `app.py` - defines tools, model, agent, and launches the UI.
- `tools/final_answer.py` - the required final answer tool the agent uses to return results.
- `requirements.txt` - Python dependencies.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Hugging Face token:
   ```bash
   $env:HF_TOKEN=your_hugging_face_token_here
   ```

## Run

```bash
python app.py
```

This launches a local Gradio web interface where you can chat with the agent.