import os
import socket

from chATLAS_Chains.log import logger
from chATLAS_Embed.EmbeddingModels import SentenceTransformerEmbedding
from chATLAS_Embed.VectorStores import PostgresParentChildVectorStore

# Keeps track of which db is stored where
db_config = {
    "cds_prod_v1": {"hostname": "dbod-chatlas-clone-20250326103412.cern.ch", "port": 6602},
    "twiki_prod": {"hostname": "dbod-chatlas.cern.ch", "port": 6624},
    "indico_prod_v1": {"hostname": "dbod-chatlas.cern.ch", "port": 6624},
}


def check_port_forwarding(host="localhost.cern.ch", port=6624):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((host, port))  # Returns 0 if connection succeeds
        if result == 0:
            logger.debug(f"Port {port} is forwarded and accessible.")
            return True
        else:
            logger.error(f"Port {port} is NOT accessible.")
            return False


def initialize_vector_store(model_path, postgres_password, db_name):
    """
    Initialises the connecton to the vector store

    Args:
        postgres_password: password, usually set at CHATLAS_DB_PASSWORD

    Returns:
        vector_store: The vector store object
    """
    logger.info(f"Instantiating vector store {db_name}")

    # Define the embedding model
    embedding_model = SentenceTransformerEmbedding(model_name=model_path)

    if os.getenv("CHATLAS_PORT_FORWARDING"):
        logger.debug("Checking port forwarding")
        server_name = "localhost.cern.ch"

        # check the port is setup properly
        port = db_config[db_name]["port"]
        if not check_port_forwarding(host=server_name, port=port):
            raise ValueError(f"Port forwarding not set up for {port}")
    else:
        logger.debug("Port forwarding not set up, connecting to DB directly")
        server_name = db_config[db_name]["hostname"]
        port = db_config[db_name]["port"]

    connection_string = f"postgresql://admin:{postgres_password}@{server_name}:{port}/{db_name}"

    # Connect to the vector store
    vectorstore = PostgresParentChildVectorStore(connection_string=connection_string, embedding_model=embedding_model)
    # Manually set search hyperparams
    vectorstore.search_hyperparams = """
            SET plan_cache_mode = force_generic_plan;
            """

    # vectorstore.explain_analyse = True
    logger.info("Vector store initialised")

    return vectorstore


# ADDITIONAL INFO
# For vectorstores can set with_timings=True to see how long queries are taking on backend for each search
# Can also set vectorstore.explain_analyse = True to return the EXPLAIN ANALYSE of a query every time before running
# which can be used to see what in query is taking the most time.

# initialize vector store
if os.getenv("CHATLAS_DB_PASSWORD") is None:
    raise ValueError("CHATLAS_DB_PASSWORD not set in environment")

if os.getenv("CHATLAS_EMBEDDING_MODEL_PATH") is None:
    raise ValueError("CHATLAS_EMBEDDING_MODEL_PATH not set in environment")
else:
    embedding_model_path = os.getenv("CHATLAS_EMBEDDING_MODEL_PATH")

twiki_vectorstore = initialize_vector_store(
    model_path=embedding_model_path, postgres_password=os.getenv("CHATLAS_DB_PASSWORD"), db_name="twiki_prod"
)
cds_vectorstore = initialize_vector_store(
    model_path=embedding_model_path, postgres_password=os.getenv("CHATLAS_DB_PASSWORD"), db_name="cds_prod_v1"
)
indico_vectorstore = initialize_vector_store(
    model_path=embedding_model_path, postgres_password=os.getenv("CHATLAS_DB_PASSWORD"), db_name="indico_prod_v1"
)

vectorstore = [twiki_vectorstore, cds_vectorstore, indico_vectorstore]
