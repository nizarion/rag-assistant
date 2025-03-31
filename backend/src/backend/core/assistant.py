from openai import AzureOpenAI
import os
from .vector_store import VectorStore

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

vector_store = VectorStore()

def get_embedding(text: str):
    response = client.embeddings.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME_EMBEDDINGS"),
        input=text
    )
    return response.data[0].embedding

# def retrieve_relevant_passages(query: str):
#     # Stubbed data for PoC
#     return ["Greek gods -- Zeus only"]

def retrieve_relevant_passages(query: str):
    query_embedding = get_embedding(query)
    return vector_store.search_similar(query_embedding)
