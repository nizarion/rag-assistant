from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import List, Any
from .logging_config import setup_logger
import uuid

logger = setup_logger(__name__)

class VectorStore:
    VECTOR_SIZE = 1536  # OpenAI embedding size

    def __init__(self, url="http://qdrant:6333"):
        self.client = QdrantClient(url=url)
        self.collection_name = "passages"
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.VECTOR_SIZE, distance=Distance.COSINE),
            )
            logger.info(f"Created collection: {self.collection_name}")
        except UnexpectedResponse as e:
            if "already exists" in str(e):
                logger.debug(f"Collection {self.collection_name} already exists")
            else:
                logger.error(f"Error creating collection: {str(e)}")
                raise

    def _validate_vectors(self, embeddings: List[List[float]]) -> bool:
        """Validate vector dimensions"""
        return all(len(embedding) == self.VECTOR_SIZE for embedding in embeddings)

    def store_passages(self, passages: List[str], embeddings: List[List[float]], batch_size: int = 100):
        """Store passages with their embeddings"""
        if not passages or not embeddings:
            raise ValueError("Passages and embeddings cannot be empty")
        
        if len(passages) != len(embeddings):
            raise ValueError("Number of passages must match number of embeddings")

        if not self._validate_vectors(embeddings):
            raise ValueError(f"All embeddings must have dimension {self.VECTOR_SIZE}")

        try:
            # Process in batches
            for i in range(0, len(passages), batch_size):
                batch_passages = passages[i:i + batch_size]
                batch_embeddings = embeddings[i:i + batch_size]
                
                points = [
                    PointStruct(
                        id=uuid.uuid4().int >> 64,  # Generate unique ID
                        vector=embedding,
                        payload={"text": passage}
                    )
                    for passage, embedding in zip(batch_passages, batch_embeddings)
                ]
                
                self.client.upsert(
                    collection_name=self.collection_name,
                    wait=True,
                    points=points
                )
                
                logger.debug(f"Stored batch of {len(points)} passages")
            
            logger.info(f"Successfully stored {len(passages)} passages")
        
        except Exception as e:
            logger.error(f"Error storing passages: {str(e)}")
            raise

    def search_similar(self, query_embedding: List[float], limit: int = 3) -> List[str]:
        """Search for similar passages"""
        if not query_embedding or len(query_embedding) != self.VECTOR_SIZE:
            raise ValueError(f"Query embedding must have dimension {self.VECTOR_SIZE}")

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
            )
            
            logger.debug(f"Found {len(results)} similar passages")
            return [hit.payload["text"] for hit in results]
            
        except Exception as e:
            logger.error(f"Error searching passages: {str(e)}")
            raise
