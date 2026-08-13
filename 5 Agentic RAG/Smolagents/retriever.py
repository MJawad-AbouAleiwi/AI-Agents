# This file is responsible for turning the gala guest list into a tool that Paul can search through.
import datasets
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from smolagents import Tool

def load_guest_documents():
    # Download the dataset
    guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

    # Convert each row into a Document
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

class GuestInfoRetrieverTool(Tool):
    """
    A tool that lets the agent search the guest list using keyword search.

    Think of this like Ctrl+F over all the guest bios, but smart enough to
    rank results by relevance instead of requiring an exact match.
    """
    name = "guest_info_retriever"
    description = "Retrieves detailed information about gala guests based on their name or relation."
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about.",
        }
    }
    output_type = "string"

    def __init__(self, docs):
        """
        Build the BM25 search index once, when the tool is created.

        Args:
            docs (list[Document]): guest documents, from load_guest_documents().
        """
        super().__init__()
        self.is_initialized = False
        self.retriever = BM25Retriever.from_documents(docs)

    def forward(self, query: str) -> str:
        """
        This is the function the agent actually calls.

        Args:
            query (str): what the agent is searching for (e.g. a guest's name).

        Returns:
            str: the top 3 matching guest entries, joined together, or a
                 "not found" message if nothing matches.
        """
        results = self.retriever.invoke(query)
        if results:
            # Only return the top 3 matches to keep the answer short and relevant
            return "\n\n".join(doc.page_content for doc in results[:3])
        return "No matching guest information found."

def build_guest_info_tool() -> GuestInfoRetrieverTool:
    """
    Convenience function: loads the data AND builds the tool in one call.

    This is what app.py imports and uses directly.
    """
    docs = load_guest_documents()
    return GuestInfoRetrieverTool(docs)