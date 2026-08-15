import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llama_index.core import Settings
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from src import config
from src.ingest import build_index

SYSTEM_PROMPT = """\
You are "Ask My Company", an internal assistant that answers employee \
questions about company policies and procedures (vacation, expenses, \
remote work, sick leave, onboarding, purchasing, IT support, etc.).

Rules you must always follow:
1. Always call the `search_company_docs` tool before answering any question \
about a policy or procedure - never answer from general knowledge or \
assumptions about what a "typical" company policy says.
2. If the tool's results don't clearly answer the question, say so plainly \
and suggest the employee contact HR or IT directly, rather than guessing.
3. Always end your final answer with the cited source document(s) exactly \
as returned by the tool, in the form: Sources: <file>, <file>.
4. Keep answers concise and specific (numbers, day counts, dollar limits, \
approval steps) rather than vague summaries.
"""

def _format_sources(source_nodes) -> str:
    seen = set()
    labels = []
    for node in source_nodes:
        meta = node.node.metadata
        fname = meta.get("file_name", "unknown source")
        page = meta.get("page_label")
        key = (fname, page)
        if key in seen:
            continue
        seen.add(key)
        labels.append(f"{fname}" + (f" (page {page})" if page else ""))
    return "; ".join(labels) if labels else "no matching source found"

def make_search_tool(query_engine) -> FunctionTool:
    def search_company_docs(question: str) -> str:
        """Search the company's actual policy and procedure documents
        (vacation, expenses, remote work, sick leave, onboarding, purchasing,
        IT support) to answer an employee's question. Always returns the
        answer together with the specific source document(s) it came from.
        Use this for every policy/procedure question - do not rely on
        general knowledge."""
        response = query_engine.query(question)
        sources = _format_sources(response.source_nodes)
        return f"{response}\n\n[Sources: {sources}]"

    return FunctionTool.from_defaults(
        fn=search_company_docs,
        name="search_company_docs",
    )

def make_list_docs_tool() -> FunctionTool:
    def list_available_documents() -> str:
        """List every company policy/procedure document currently indexed
        and available to search. Useful when an employee asks what topics
        are covered, or when a search comes back empty."""
        lines = []
        for root, _, files in os.walk(config.DATA_DIR):
            for f in files:
                if f.startswith("."):
                    continue
                rel = os.path.relpath(os.path.join(root, f), config.DATA_DIR)
                lines.append(rel)
        return "\n".join(sorted(lines)) if lines else "No documents indexed yet."

    return FunctionTool.from_defaults(fn=list_available_documents)

def build_agent(force_rebuild: bool = False) -> FunctionAgent:
    index = build_index(force_rebuild=force_rebuild)
    query_engine = index.as_query_engine(similarity_top_k=config.SIMILARITY_TOP_K)
    tools = [make_search_tool(query_engine), make_list_docs_tool()]
    agent = FunctionAgent(
        tools=tools,
        llm=Settings.llm,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

if __name__ == "__main__":
    import asyncio

    async def _demo():
        a = build_agent()
        result = await a.run("What documents do you have access to?")
        print(result)

    asyncio.run(_demo())