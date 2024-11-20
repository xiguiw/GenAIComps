export host_ip=10.239.182.158
export TEI_EMBEDDING_ENDPOINT=http://${host_ip}:6006
export HUGGINGFACEHUB_API_TOKEN=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
export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"

export POSTGRES_USER=testuser
export POSTGRES_PASSWORD=testpwd
export POSTGRES_DB=vectordb


export PG_CONNECTION_STRING=postgresql+psycopg2://testuser:testpwd@${host_ip}:5432/vectordb
export PG_INDEX_NAME="pgvct_index"
