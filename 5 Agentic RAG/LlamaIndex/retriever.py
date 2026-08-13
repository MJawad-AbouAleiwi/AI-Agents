# This file is responsible for turning the gala guest list into a tool that Paul can search through.
import datasets
from llama_index.core.schema import Document
from llama_index.core.tools import FunctionTool
from llama_index.retrievers.bm25 import BM25Retriever

def load_guest_documents():
    # Download the dataset
    guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

    # Convert each row into a Document the retriever can search
    docs = [
        Document(
            text="\n".join(
                [
                    f"Name: {guest_dataset['name'][i]}",
                    f"Relation: {guest_dataset['relation'][i]}",
                    f"Description: {guest_dataset['description'][i]}",
                    f"Email: {guest_dataset['email'][i]}",
                ]
            ),
            metadata={"name": guest_dataset["name"][i]},
        )
        for i in range(len(guest_dataset))
    ]
    return docs

def build_guest_info_tool() -> FunctionTool:
    """
    Loads the guest data, builds a BM25 search index over it, and wraps
    that search in a FunctionTool that Paul can call.

    This is what app.py imports and uses directly.
    """
    docs = load_guest_documents()

    # Build the BM25 keyword-search index once, over all guest documents.
    bm25_retriever = BM25Retriever.from_defaults(nodes=docs)

    def get_guest_info_retriever(query: str) -> str:
        """Retrieves detailed information about gala guests based on their name or relation."""
        results = bm25_retriever.retrieve(query)
        if results:
            # Only return the top 3 matches to keep the answer short and relevant
            return "\n\n".join(doc.text for doc in results[:3])
        return "No matching guest information found."

    # Wrap the plain Python function as a tool the agent can call
    return FunctionTool.from_defaults(get_guest_info_retriever)