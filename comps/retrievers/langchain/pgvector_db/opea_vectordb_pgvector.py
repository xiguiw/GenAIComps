import os
import asyncio

#from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from os import PathLike

from langchain_core.documents.base import Document
from langchain_core.embeddings.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings # Pgvector embedding

#from opea_vectordb_interface import OpeaVectorDatabase
from retrievers.langchain.db_interface.opea_vectordb_interface import OpeaVectorDatabase

tei_embedding_endpoint = os.getenv("TEI_EMBEDDING_ENDPOINT")

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

from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from .config import EMBED_MODEL, PG_INDEX_NAME, PG_CONNECTION_STRING, PG_PORT, HUG_API_TOKEN

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

if (True):
    pg_db = PGvector_OpeaVectorDatabase()
    retriever2 = opea_Retrieval(vector_db=pg_db)
    import random
    vec_embedding = [random.uniform(-1, 1) for _ in range(768)]
    print(vec_embedding)

    asyncio.run(retriever2.retrieval("similarity", vec_embedding)) 

