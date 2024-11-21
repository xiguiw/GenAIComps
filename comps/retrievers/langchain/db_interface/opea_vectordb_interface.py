import os

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from os import PathLike

from langchain_core.documents.base import Document
from langchain_core.embeddings.embeddings import Embeddings

tei_embedding_endpoint = os.getenv("TEI_EMBEDDING_ENDPOINT")

# Opea Vectore Database Interface. Any Vector DB to be integrated into OPEA, it needs to derivate the class and implements these interfaces
class OpeaVectorDatabase(ABC):
    """
    Create a vectorstore from a list of texts.
    This is a user-friendly interface that:
    1) Embeds documents.
    2) Creates a new Redis index if it doesn’t already exist
    3) Adds the documents to the newly created Redis index.
    """
    @abstractmethod
    def ingest_text_and_create_vector_store(
        self,
        texts: List[str],
        embedding: Embeddings,  # Replace with the actual type if available
        metadatas: Union[List[Dict], None] = None,
        index_name: Union[str, None] = None,
        index_schema: Union[Dict[str, List[Dict[str, str]]], str, PathLike, None] = None,
        vector_schema: Union[Dict[str, Union[str, int]], None] = None,
        vector_url: Union[str, None] = None,
        **kwargs: Any
    ) -> 'OpeaVectorDatabase':  # Replace with the actual return type if available
        """
        Abstract method for ingesting text and creating a vector store.

        Args:
            texts (List[str]): List of text documents to be ingested.
            embedding (Embeddings): Embedding model or object for vectorization.
            metadatas (Union[List[Dict], None], optional): Metadata for the texts. Defaults to None.
            index_name (Union[str, None], optional): Name of the index. Defaults to None.
            index_schema (Union[Dict[str, List[Dict[str, str]]], str, PathLike, None], optional): Schema for the index. Defaults to None.
            vector_schema (Union[Dict[str, Union[str, int]], None], optional): Schema for vectors. Defaults to None.
            vector_url (Union[str, None], optional): URL of the vector store. Defaults to None.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            OpeaVectorDatabase: The created vector database object.
        """
        pass
    """
    def ingest_text_and_create_vector_store(texts: list[str], embedding: Embeddings, metadatas: list[dict] | None = None, index_name: str | None = None, index_schema: Dict[str, list[Dict[str, str]]] | str | PathLike | None = None, vector_schema: Dict[str, str | int] | None = None, vector_url: str | None = None, **kwargs: Any) -> OpeaVectorDatabase:
        pass
    """

    @abstractmethod
    async def asimilarity_search_by_vector(self, embedding: list[float], k: int = 4, **kwargs: Any) -> list[Document]:
        """Search for the top-k closest vectors to the query vector."""
        pass

    @abstractmethod
    def is_db_empty(self) -> bool:
        """Insert a vector into the database."""
        pass
    '''
    @abstractmethod
    async def asimilarity_search_with_relevance_scores(query: str, k: int = 4, **kwargs: Any) → list[tuple[Document, float]]
        pass

    @abstractmethod
    async def amax_marginal_relevance_search(query: str, k: int = 4, fetch_k: int = 20, lambda_mult: float = 0.5, **kwargs: Any) → list[Document]
        pass
    '''
