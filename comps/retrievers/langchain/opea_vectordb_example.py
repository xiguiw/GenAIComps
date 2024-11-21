import os
import asyncio

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from os import PathLike

from langchain_core.documents.base import Document
from langchain_core.embeddings.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings # Pgvector embedding

from redis_config import EMBED_MODEL, INDEX_NAME, REDIS_URL
from comps import (
    CustomLogger,
    EmbedDoc,
    SearchedDoc,
    ServiceType,
    TextDoc,
)

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

# Opea Retrieval interact with OpeaVectorDatabase
class opea_Retrieval:
    def __init__(self, vector_db: OpeaVectorDatabase):
        self.vector_db = vector_db

    async def retrieval(self, search_type: str, embedding: list,  top_k: int = 3) -> list[Document]:
        """Insert a vector into the underlying database."""
        search_res = []
        #import pdb
        #pdb.set_trace()
        search_res = await self.vector_db.asimilarity_search_by_vector(embedding=embedding, top_k=top_k)
        print("search_res: ", search_res)
        return search_res 

from langchain_community.vectorstores import Redis, PGVector
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from config import EMBED_MODEL, PG_INDEX_NAME, PG_CONNECTION_STRING, PG_PORT, HUG_API_TOKEN 

class PGvector_OpeaVectorDatabase(OpeaVectorDatabase):
    def __init__(self):
        if tei_embedding_endpoint:
            # create embeddings using TEI endpoint service
            embeddings = HuggingFaceHubEmbeddings(model=tei_embedding_endpoint)
            #embeddings = HuggingFaceEndpointEmbeddings(model=tei_embedding_endpoint)
        else:
            # create embeddings using local embedding model
            embeddings = HuggingFaceBgeEmbeddings(model_name=EMBED_MODEL)

        self.vector_db = PGVector(
            embedding_function=embeddings,
            collection_name=PG_INDEX_NAME,
            connection_string=PG_CONNECTION_STRING,)
        return 

    def ingest_text_and_create_vector_store(texts: list[str], embedding: Embeddings, metadatas: list[dict] | None = None, index_name: str | None = None, index_schema: Dict[str, list[Dict[str, str]]] | str | PathLike | None = None, vector_schema: Dict[str, str | int] | None = None, **kwargs: Any) -> OpeaVectorDatabase:
        _ = self.vector_db.from_texts(
            texts=texts,
            embedding=embedding,
            index_name=INDEX_NAME,
            vector_url=REDIS_URL,
        )
        print(f"Processed batch text")

    async def asimilarity_search_by_vector(self, embedding: list[float], k: int = 4, **kwargs: Any) -> list[Document]:
       search_res = await self.vector_db.asimilarity_search_by_vector(embedding, k=k)
       #search_res = await self.vector_db.asimilarity_search_by_vector(embedding=input.embedding)
       return search_res 

    def is_db_empty(self) -> bool:
        pass

from langchain_huggingface import HuggingFaceEndpointEmbeddings # Redis embedding
class Redis_OpeaVectorDatabase(OpeaVectorDatabase):
    def __init__(self):
        if tei_embedding_endpoint:
            # create embeddings using TEI endpoint service
            #embeddings = HuggingFaceHubEmbeddings(model=tei_embedding_endpoint)
            embeddings = HuggingFaceEndpointEmbeddings(model=tei_embedding_endpoint)
        else:
            # create embeddings using local embedding model
            embeddings = HuggingFaceBgeEmbeddings(model_name=EMBED_MODEL)

        self.vector_db = Redis(embedding=embeddings, index_name=INDEX_NAME, redis_url=REDIS_URL)

        return 

    async def asimilarity_search_by_vector(self, embedding: list[float], k: int = 4, **kwargs: Any) -> list[Document]:
       search_res = await self.vector_db.asimilarity_search_by_vector(embedding, k=k)
       return search_res 

    def is_db_empty(self) -> bool:
        if (self.vector_db.client.keys() == []):
            return True
        else:
            return False

    def ingest_text_and_create_vector_store(texts: list[str], embedding: Embeddings, metadatas: list[dict] | None = None, index_name: str | None = None, index_schema: Dict[str, list[Dict[str, str]]] | str | PathLike | None = None, vector_schema: Dict[str, str | int] | None = None, **kwargs: Any) -> OpeaVectorDatabase:
        _ = self.vector_db.from_texts(
            texts=texts,
            embedding=embedding,
            index_name=INDEX_NAME,
            vector_url=REDIS_URL,
        )
        print(f"Processed batch text")

    async def asimilarity_search_by_vector(self, embedding: list[float], k: int = 4, **kwargs: Any) -> list[Document]:
       search_res = await self.vector_db.asimilarity_search_by_vector(embedding, k=k)
       return search_res 

    def is_db_empty(self) -> bool:
        if (self.vector_db.client.keys() == []):
            return True
        else:
            return False

if (False):
    redis_db = Redis_OpeaVectorDatabase()
    pg_db = PGvector_OpeaVectorDatabase()
    retriever = opea_Retrieval(vector_db=redis_db)
    retriever2 = opea_Retrieval(vector_db=pg_db)
    import random
    vec_embedding = [random.uniform(-1, 1) for _ in range(768)]
    print(vec_embedding)

    asyncio.run(retriever2.retrieval("similarity", vec_embedding)) 

