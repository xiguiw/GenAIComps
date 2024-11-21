import os
import asyncio

#from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from os import PathLike

from langchain_core.documents.base import Document
from langchain_core.embeddings.embeddings import Embeddings

from .milvus_config import (
    COLLECTION_NAME,
    LOCAL_EMBEDDING_MODEL,
    MILVUS_HOST,
    MILVUS_PORT,
    MOSEC_EMBEDDING_ENDPOINT,
    MOSEC_EMBEDDING_MODEL,
    TEI_EMBEDDING_ENDPOINT,
)
#from ..db_interface.opea_vectordb_interface import OpeaVectorDatabase
from retrievers.langchain.db_interface.opea_vectordb_interface import OpeaVectorDatabase


from langchain_community.embeddings import HuggingFaceBgeEmbeddings, HuggingFaceHubEmbeddings
from langchain_milvus.vectorstores import Milvus

tei_embedding_endpoint = os.getenv("TEI_EMBEDDING_ENDPOINT")

class Milvus_OpeaVectorDatabase(OpeaVectorDatabase):
    def __init__(self):
        if TEI_EMBEDDING_ENDPOINT:
            # create embeddings using TEI endpoint service
            embeddings = HuggingFaceHubEmbeddings(model=TEI_EMBEDDING_ENDPOINT)
            print("embeddings info:", embeddings)
        else:
            # create embeddings using local embedding model
            embeddings = HuggingFaceBgeEmbeddings(model_name=LOCAL_EMBEDDING_MODEL)

        url = "http://" + str(MILVUS_HOST) + ":" + str(MILVUS_PORT)
        self.vector_db = Milvus(
            embeddings,
            connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT, "uri": url},
            collection_name=COLLECTION_NAME,
        )

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

if (True):
    milvus = Milvus_OpeaVectorDatabase()
    retriever = opea_Retrieval(vector_db=milvus)
    import random
    vec_embedding = [random.uniform(-1, 1) for _ in range(768)]
    print(vec_embedding)

    asyncio.run(retriever.retrieval("similarity", vec_embedding)) 
