# Debate Court (Using LangGraph)

An Advocate and Opponent argue a controversial claim with evidence, before delivering a final verdict.

```
                 CLAIM
                   │
          ┌────────┴────────┐
          ↓                 ↓
      Advocate           Opponent
          │                 │
          ↓                 ↓
      Evidence           Evidence
          │                 │
          └────────┬────────┘
                    ↓
                  Judge
                    ↓
           Weaknesses Found? ──No──> Final Verdict
                    │Yes
                    ↓
             Re-debate
```

## Setup

1. **Install Ollama**: https://ollama.com/download

2. **Pull the Model**:
   ```bash
   ollama pull llama3.2
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the default example claim:
```bash
python main.py
```

Run a claim, capped at 2 rounds:
```bash
python main.py "Universal basic income would reduce poverty more than existing welfare systems." --max-rounds 2
```

Save the full transcript as JSON:
```bash
python main.py "Open-source LLMs will surpass proprietary models." --out transcript.json
```

## Project Structure

```
debate_court/
├── config.py     # Model, memory, and round settings
├── state.py      # LangGraph state schema
├── prompts.py    # System prompts
├── llm.py        # Ollama wrapper
├── nodes.py      # Node functions
├── graph.py      # StateGraph wiring
├── main.py       # Run a debate, print transcript, inject evidence
├── requirements.txt
```

## How the Judge Stays Honest

The judge is explicitly instructed not to pick a winner by tone or confidence. 

It must score both sides 1-10 on five separate axes
(`evidence_quality`, `logical_consistency`, `unsupported_assumptions`,
`contradictions`, `source_reliability`), and can only send the debate back
for another round if it names specific weaknesses and which side needs to address them. 

The final verdict node then looks at the entire per-round record, not just the last exchange,
so a side that fixed its weaknesses across rounds is rewarded and a side that kept repeating the same flaw is penalized.