# Dummy Agent

A small, educational notebook that shows how a tool-using AI agent works,
without using an agent framework.

## What It Does

1. **Serverless API** - Connects to the [Kimi-K2.5](https://huggingface.co/moonshotai/Kimi-K2.5)
   model via Hugging Face's serverless Inference API and sends a simple chat request.
2. **Dummy Agent** - Implements a minimal ReAct-style loop:
   - A system prompt describes one tool and the exact format the model must follow.
   - We show what happens when the model is left to complete the whole loop on its own.
   - We then use a stop sequence to make the model pause right after deciding on an action, so we can intercept it.
   - A real Python function is executed locally to produce the actual tool result.
   - That real result is appended to the conversation, and the model is called again to produce a final answer.

This illustrates the core idea behind tool-calling agents: the LLM only
decides what to do - your code is responsible for actually doing it and
feeding the result back in.

## Requirements

```bash
pip install -r requirements.txt
```

## Setup

The notebook expects a Hugging Face API token, loaded from a local `.env` file.

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste in your real token:
   ```
   HF_TOKEN=hf_your_real_token_here
   ```
3. The notebook calls `load_dotenv()` at the top, which reads
   `.env` and makes `HF_TOKEN` available via `os.environ`.

`.env` is already listed in `.gitignore` so it won't get committed by accident.