# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import time
from typing import Union

#from opea_vectordb import PGvector_OpeaVectorDatabase, Redis_OpeaVectorDatabase, opea_Retrieval    
#from opea_vectordb_interface

from comps import (
    CustomLogger,
    EmbedDoc,
    SearchedDoc,
    ServiceType,
    TextDoc,
    opea_microservices,
    register_microservice,
    register_statistics,
    statistics_dict,
)
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    RetrievalRequest,
    RetrievalResponse,
    RetrievalResponseData,
)

logger = CustomLogger("retriever_redis")
logflag = os.getenv("LOGFLAG", False)

tei_embedding_endpoint = os.getenv("TEI_EMBEDDING_ENDPOINT")
db_type = os.getenv("DB_TYPE", "redis")

if (db_type == "REDIS"):
    from redis_db.opea_vectordb_redis import Redis_OpeaVectorDatabase, opea_Retrieval
elif (db_type == "PGVECTOR"):
    from pgvector_db.opea_vectordb_pgvector import PGvector_OpeaVectorDatabase, opea_Retrieval
else:
    print("NOT support db:", db_type)
    exit()

@register_microservice(
    name="opea_service@retriever_redis",
    service_type=ServiceType.RETRIEVER,
    endpoint="/v1/retrieval",
    host="0.0.0.0",
    port=7000,
)

# Opea Retrieval interact with OpeaVectorDatabase
#class OpeaRetrieval:
#    def __init__(self, vector_db: OpeaVectorDatabase):
#        self.vector_db = vector_db

@register_statistics(names=["opea_service@retriever_redis"])
async def retrieve(
    input: Union[EmbedDoc, RetrievalRequest, ChatCompletionRequest]
) -> Union[SearchedDoc, RetrievalResponse, ChatCompletionRequest]:
    if logflag:
        logger.info(input)
    start = time.time()
    # check if the Redis index has data
    #if vector_db.client.keys() == []:
    #    search_res = []
    #else:
    if (True):
        if isinstance(input, EmbedDoc):
            query = input.text
        else:
            # for RetrievalRequest, ChatCompletionRequest
            query = input.input
        # if the Redis index has data, perform the search
        search_res = await retriever.vector_db.asimilarity_search_by_vector(embedding=input.embedding, k=3)
        print(input.embedding)
        print("search_res: ", search_res)
        '''
        if input.search_type == "similarity":
            search_res = await vector_db.asimilarity_search_by_vector(embedding=input.embedding, k=input.k)
        elif input.search_type == "similarity_distance_threshold":
            if input.distance_threshold is None:
                raise ValueError("distance_threshold must be provided for " + "similarity_distance_threshold retriever")
            search_res = await vector_db.asimilarity_search_by_vector(
                embedding=input.embedding, k=input.k, distance_threshold=input.distance_threshold
            )
        elif input.search_type == "similarity_score_threshold":
            docs_and_similarities = await vector_db.asimilarity_search_with_relevance_scores(
                query=input.text, k=input.k, score_threshold=input.score_threshold
            )
            search_res = [doc for doc, _ in docs_and_similarities]
        elif input.search_type == "mmr":
            search_res = await vector_db.amax_marginal_relevance_search(
                query=input.text, k=input.k, fetch_k=input.fetch_k, lambda_mult=input.lambda_mult
            )
        else:
            raise ValueError(f"{input.search_type} not valid")
        '''

    # return different response format
    retrieved_docs = []
    if isinstance(input, EmbedDoc):
        for r in search_res:
            retrieved_docs.append(TextDoc(text=r.page_content))
        result = SearchedDoc(retrieved_docs=retrieved_docs, initial_query=input.text)
    else:
        for r in search_res:
            retrieved_docs.append(RetrievalResponseData(text=r.page_content, metadata=r.metadata))
        if isinstance(input, RetrievalRequest):
            result = RetrievalResponse(retrieved_docs=retrieved_docs)
        elif isinstance(input, ChatCompletionRequest):
            input.retrieved_docs = retrieved_docs
            input.documents = [doc.text for doc in retrieved_docs]
            result = input

    statistics_dict["opea_service@retriever_redis"].append_latency(time.time() - start, None)
    if logflag:
        logger.info(result)
    return result

if __name__ == "__main__":
    # Create vectorstore
    if (db_type == "REDIS"):
        opea_db = Redis_OpeaVectorDatabase()
    elif (db_type == "PGVECTOR"):
        opea_db = PGvector_OpeaVectorDatabase()
    else:
        print("NOT support db:", db_type)
        exit()
    #retriever = opea_Retrieval(vector_db=pg_db)
    retriever = opea_Retrieval(vector_db=opea_db)
    opea_microservices["opea_service@retriever_redis"].start()
