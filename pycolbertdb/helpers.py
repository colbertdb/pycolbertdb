"""Helper functions for working with pycolbertdb."""

from typing import List
from llama_index.core import Document

from pycolbertdb.models import CreateCollectionDocument


def from_llama_index_documents(
    documents: List[Document],
) -> List[CreateCollectionDocument]:
    """Converts a list of llama_index Documents to a list of dictionaries with the same content and metadata."""
    output = []
    for document in documents:
        metadata = document.metadata
        metadata["source"] = document.id_
        output_document = CreateCollectionDocument(
            content=document.text, metadata=metadata
        )
        output.append(output_document)
    return output
