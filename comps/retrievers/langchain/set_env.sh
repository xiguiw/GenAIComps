export host_ip=$(hostname -i)
export TEI_EMBEDDING_ENDPOINT=http://${host_ip}:6006
export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"

export POSTGRES_USER=testuser
export POSTGRES_PASSWORD=testpwd
export POSTGRES_DB=vectordb

export DB_TYPE="REDIS"
export #DB_TYPE="PGVECTOR"

export PG_CONNECTION_STRING=postgresql+psycopg2://testuser:testpwd@${host_ip}:5432/vectordb
export PG_INDEX_NAME="pgvct_index"
export PYTHONPATH=$PYTHONPATH,/home/xiguiwan/OPEA/fork-GenAIComps/comps
