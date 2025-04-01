from dataclasses import dataclass
from typing import final, TypeAlias, TypeGuard
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, ScoredPoint
from qdrant_client.http.exceptions import UnexpectedResponse
from .logging_config import setup_logger
import uuid

logger = setup_logger(__name__)

# Type aliases for clarity
Embedding: TypeAlias = list[float]
Embeddings: TypeAlias = list[Embedding]
Passages: TypeAlias = list[str]

# Constants
DEFAULT_URL = "http://qdrant:6333"
DEFAULT_BATCH_SIZE = 100
DEFAULT_SEARCH_LIMIT = 3
VECTOR_SIZE = 1536  # OpenAI embedding size


@dataclass(frozen=True)
class VectorConfig:
    """Vector store configuration."""

    vector_size: int = VECTOR_SIZE
    collection_name: str = "passages"
    distance: Distance = Distance.COSINE

    @classmethod
    def default(cls) -> "VectorConfig":
        """Create default configuration."""
        return cls()


class VectorStoreError(Exception):
    """Base exception for vector store errors."""

    pass


@final
class VectorStore:
    """Vector store for managing embeddings and passages."""

    def __init__(
        self, url: str = DEFAULT_URL, config: VectorConfig | None = None
    ) -> None:
        """Initialize vector store with client and configuration."""
        self.client = QdrantClient(url=url)
        self.config = config or VectorConfig.default()
        self._init_collection()

    # Public API methods
    def store_passages(
        self,
        passages: Passages,
        embeddings: Embeddings,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        """Store passages with their embeddings in batches."""
        if not self._validate_inputs(passages, embeddings):
            raise ValueError("Invalid passages or embeddings")

        try:
            for i in range(0, len(passages), batch_size):
                batch_passages = passages[i : i + batch_size]
                batch_embeddings = embeddings[i : i + batch_size]
                self._store_batch(batch_passages, batch_embeddings)

            logger.info(f"Successfully stored {len(passages)} passages")
        except Exception as e:
            raise VectorStoreError(f"Failed to store passages: {e}") from e

    def search_similar(
        self, query: Embedding, limit: int = DEFAULT_SEARCH_LIMIT
    ) -> Passages:
        """Find similar passages using query embedding."""
        if not self._is_valid_embedding(query):
            raise ValueError(f"Query must have dimension {self.config.vector_size}")

        try:
            results = self.client.search(
                collection_name=self.config.collection_name,
                query_vector=query,
                limit=limit,
            )
            return self._extract_passages(results)
        except Exception as e:
            raise VectorStoreError(f"Search failed: {e}") from e

    # Private helper methods
    def _init_collection(self) -> None:
        """Create collection if it doesn't exist."""
        try:
            _ = self.client.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=VectorParams(
                    size=self.config.vector_size, distance=self.config.distance
                ),
            )
            logger.info(f"Created collection: {self.config.collection_name}")
        except UnexpectedResponse as e:
            if "already exists" in str(e):
                logger.debug(f"Collection {self.config.collection_name} exists")
                return
            raise VectorStoreError(f"Failed to create collection: {e}") from e

    def _store_batch(self, passages: Passages, embeddings: Embeddings) -> None:
        """Store a single batch of passages and embeddings."""
        points = [
            PointStruct(
                id=uuid.uuid4().int >> 64, vector=embedding, payload={"text": passage}
            )
            for passage, embedding in zip(passages, embeddings)
        ]
        _ = self.client.upsert(
            collection_name=self.config.collection_name, wait=True, points=points
        )
        logger.debug(f"Stored batch of {len(points)} passages")

    def _extract_passages(self, results: list[ScoredPoint]) -> Passages:
        """Extract valid passages from search results."""
        if not results:
            logger.debug("No similar passages found")
            return []

        passages = [
            text
            for hit in results
            if (text := hit.payload.get("text")) and isinstance(text, str)
        ]
        logger.debug(
            f"Found {len(passages)} valid passages from {len(results)} results"
        )
        return passages

    # Validation methods
    def _is_valid_embedding(self, embedding: Embedding) -> TypeGuard[Embedding]:
        """Check if embedding has correct dimension."""
        return len(embedding) == self.config.vector_size

    def _validate_inputs(self, passages: Passages, embeddings: Embeddings) -> bool:
        """Validate input passages and embeddings."""
        return (
            bool(passages)
            and bool(embeddings)
            and len(passages) == len(embeddings)
            and all(self._is_valid_embedding(emb) for emb in embeddings)
        )
