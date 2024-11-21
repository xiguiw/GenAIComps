export host_ip=$(hostname -i)
export TEI_EMBEDDING_ENDPOINT=http://${host_ip}:6006
export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"

export POSTGRES_USER=testuser
export POSTGRES_PASSWORD=testpwd
export POSTGRES_DB=vectordb

export PG_CONNECTION_STRING=postgresql+psycopg2://testuser:testpwd@${host_ip}:5432/vectordb
export PG_INDEX_NAME="pgvct_index"
export PYTHONPATH=/home/xiguiwan/OPEA/fork-GenAIComps:/home/xiguiwan/OPEA/fork-GenAIComps/comps

# Get the first argument
DB_TYPE=${1:-"REDIS"}
#"REDIS"
#export DB_TYPE="MILVUS"
#export DB_TYPE="PGVECTOR"

# Define allowed values
ALLOWED_VALUES=("REDIS" "MILVUS" "PGVECTOR")

# Check if the provided value is in the allowed list
if [[ " ${ALLOWED_VALUES[@]} " =~ " ${DB_TYPE} " ]]; then
    # If valid, export the value
    export DB_TYPE
    echo "Database type set to: $DB_TYPE"
else
    # If invalid, print an error and exit
    echo "Error: Invalid database type '${DB_TYPE}'. Allowed values are: ${ALLOWED_VALUES[*]}"
    return 1  # Exit with an error code in case of source
fi

if [[ -z "${HUGGINGFACEHUB_API_TOKEN}" ]]; then
    echo "Error: Environment variable HUGGINGFACEHUB_API_TOKEN is not set."
    return 1  # Exit with a non-zero status to indicate failure
fi
