# The LlamaIndex Framewrok

This repository contains two companion notebooks demonstrating how to build agents and agentic workflows using [LlamaIndex](https://www.llamaindex.ai/).

## Contents

### 1. `Agents_LlamaIndex.ipynb` - Using Agents in LlamaIndex

This notebook focuses on building and using agents in LlamaIndex.

### 2. `Agentic_Workflows_LlamaIndex.ipynb` - Creating Agentic Workflows

This notebook introduces LlamaIndex's Workflow framework from the ground up.

## Requirements

```bash
pip install llama-index llama-index-llms-huggingface-api llama-index-embeddings-huggingface
```

You will also need a Hugging Face API token to use `HuggingFaceInferenceAPI`. Set it when instantiating the LLM:

```python
llm = HuggingFaceInferenceAPI(
    model_name="meta-llama/Llama-3.2-3B-Instruct",
    token="",
)
```

## Usage

Open either notebook in Jupyter or Google Colab and run the cells in order.

```bash
jupyter notebook Agents_LlamaIndex.ipynb
jupyter notebook Agentic_Workflows_LlamaIndex.ipynb
```