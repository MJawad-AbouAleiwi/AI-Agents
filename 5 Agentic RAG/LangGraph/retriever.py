# This file is responsible for turning the gala guest list into a tool that Paul can search through.
import datasets
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.tools import Tool

def load_guest_documents():
    # Download the dataset
    guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

    # Convert each row into a Document the retriever can search
    docs = [
        Document(
            page_content="\n".join(
                [
                    f"Name: {guest['name']}",
                    f"Relation: {guest['relation']}",
                    f"Description: {guest['description']}",
                    f"Email: {guest['email']}",
                ]
            ),
            metadata={"name": guest["name"]},
        )
        for guest in guest_dataset
    ]
    return docs

def build_guest_info_tool() -> Tool:
    """
    Loads the guest data, builds a BM25 search index over it, and wraps
    that search in a LangChain Tool that Paul can call.

    This is what app.py imports and uses directly.
    """
    docs = load_guest_documents()

    # Build the BM25 keyword-search index once, over all guest documents.
    bm25_retriever = BM25Retriever.from_documents(docs)

    def extract_text(query: str) -> str:
        """Retrieves detailed information about gala guests based on their name or relation."""
        results = bm25_retriever.invoke(query)
        if results:
            # Only return the top 3 matches to keep the answer short and relevant
            return "\n\n".join(doc.page_content for doc in results[:3])
        return "No matching guest information found."

    # Wrap the plain Python function as a tool the agent can call
    return Tool(
        name="guest_info_retriever",
        func=extract_text,
        description="Retrieves detailed information about gala guests based on their name or relation.",
    )