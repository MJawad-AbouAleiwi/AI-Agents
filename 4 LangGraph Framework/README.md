# Email Processing System (LangGraph Agent)

A small LangGraph agent that reads an incoming email, classifies it as spam or
legitimateusing a local LLM (via Ollama), and either discards spam or drafts a
reply for legitimate messages.

## How it works

```
START -> read_email -> classify_email --spam--> handle_spam -> END
                                        \
                                         --legitimate--> draft_response -> notify_receiver -> END
```

- **read_email** - logs the incoming email.
- **classify_email** - asks the LLM to label the email.
- **route_email** - conditional edge that sends the email down the spam or
  legitimate path based on the classification.
- **handle_spam** - logs that the email was discarded, with a reason.
- **draft_response** - asks the LLM to draft a reply.
- **notify_receiver** - prints the draft for the user to review.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally with the `llama3.2` model pulled
  (`ollama pull llama3.2`)
- `langgraph`, `langchain-ollama`, `langchain-core`

## Running it

Open `Email_Processing_System.ipynb` and run all cells. 