from openai import AzureOpenAI
import os
from .logging_config import setup_logger

logger = setup_logger(__name__)


def create_azure_client(endpoint: str) -> AzureOpenAI:
    """Create an Azure OpenAI client with the given endpoint."""
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        azure_endpoint=endpoint,
    )


# Create clients for different endpoints
chat_client = create_azure_client(os.getenv("AZURE_OPENAI_ENDPOINT") or "changeme")
embeddings_client = create_azure_client(
    os.getenv("AZURE_OPENAI_ENDPOINT") or "changeme"
)
