from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class VectorStore:
    def __init__(self, url="http://qdrant:6333"):
        self.client = QdrantClient(url=url)
        self.collection_name = "passages"
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        except Exception:
            # Collection might already exist
            pass

    def store_passages(self, passages, embeddings):
        """Store passages with their embeddings"""
        points = [
            PointStruct(id=idx, vector=embedding, payload={"text": passage})
            for idx, (passage, embedding) in enumerate(zip(passages, embeddings))
        ]
        self.client.upsert(
            collection_name=self.collection_name, wait=True, points=points
        )

    def search_similar(self, query_embedding, limit=3):
        """Search for similar passages"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )
        return [hit.payload["text"] for hit in results]
