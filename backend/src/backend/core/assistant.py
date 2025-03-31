import os
from .vector_store import VectorStore
from .logging_config import setup_logger
from .azure_client import embeddings_client

logger = setup_logger(__name__)
vector_store = VectorStore()


def get_embedding(text: str):
    logger.info(f"Generating embedding for text: {text[:50]}...")
    response = embeddings_client.embeddings.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME_EMBEDDINGS"), input=text
    )
    logger.debug("Embedding generated successfully")
    return response.data[0].embedding


def retrieve_relevant_passages(query: str):
    logger.info(f"Retrieving passages for query: {query}")
    query_embedding = get_embedding(query)
    similar_passages = vector_store.search_similar(query_embedding)
    logger.info(f"Found {len(similar_passages)} relevant passages")
    return similar_passages
