from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import logging
import uuid

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Handles vector storage and similarity search using Qdrant
    """

    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "textbook_chunks"):
        """
        Initialize the vector store with Qdrant connection
        """
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client: Optional[QdrantClient] = None
        logger.info(f"VectorStore configured for collection: {collection_name}")

    def _get_client(self):
        """
        Get the Qdrant client, creating it if it doesn't exist
        """
        if self.client is None:
            self.client = QdrantClient(host=self.host, port=self.port)
            self._create_collection()
        return self.client

    def _create_collection(self):
        """
        Create the collection in Qdrant if it doesn't exist
        """
        try:
            # Check if collection exists
            self._get_client().get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")
        except:
            # Create new collection
            self._get_client().create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Size for all-MiniLM-L6-v2 embeddings
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection {self.collection_name}")

    def store_chunk(self, chunk_id: str, embedding: List[float], content: str, metadata: Dict[str, Any] = None):
        """
        Store a content chunk with its embedding in the vector database
        """
        try:
            self._get_client().upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=chunk_id,
                        vector=embedding,
                        payload={
                            "content": content,
                            "metadata": metadata or {}
                        }
                    )
                ]
            )
            logger.debug(f"Stored chunk {chunk_id} in vector store")
        except Exception as e:
            logger.error(f"Error storing chunk {chunk_id}: {str(e)}")
            raise

    def store_chunks(self, chunks_data: List[Dict[str, Any]]):
        """
        Store multiple content chunks with their embeddings
        """
        points = []
        for chunk_data in chunks_data:
            point = models.PointStruct(
                id=chunk_data["chunk_id"],
                vector=chunk_data["embedding"],
                payload={
                    "content": chunk_data["content"],
                    "metadata": chunk_data.get("metadata", {})
                }
            )
            points.append(point)

        try:
            self._get_client().upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Stored {len(chunks_data)} chunks in vector store")
        except Exception as e:
            logger.error(f"Error storing chunks: {str(e)}")
            raise

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar content chunks based on query embedding
        Returns top N most similar chunks with their content and metadata
        """
        try:
            results = self._get_client().search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            similar_chunks = []
            for result in results:
                similar_chunks.append({
                    "id": result.id,
                    "content": result.payload["content"],
                    "metadata": result.payload["metadata"],
                    "similarity_score":.
                    result.score
                })

            logger.debug(f"Found {len(similar_chunks)} similar chunks")
            return similar_chunks
        except Exception as e:
            logger.error(f"Error searching for similar chunks: {str(e)}")
            raise

    def delete_chunk(self, chunk_id: str):
        """
        Delete a specific chunk from the vector store
        """
        try:
            self._get_client().delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[chunk_id]
                )
            )
            logger.debug(f"Deleted chunk {chunk_id} from vector store")
        except Exception as e:
            logger.error(f"Error deleting chunk {chunk_id}: {str(e)}")
            raise

    def clear_collection(self):
        """
        Clear all vectors from the collection (use with caution!)
        """
        try:
            # Get all point IDs
            all_points = self._get_client().scroll(
                collection_name=self.collection_name,
                limit=10000  # Adjust based on expected collection size
            )[0]

            point_ids = [point.id for point in all_points]

            if point_ids:
                self._get_client().delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=point_ids
                    )
                )
                logger.info(f"Cleared {len(point_ids)} points from collection")
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    # Initialize vector store
    vector_store = VectorStore()

    # Example embeddings (in practice, these would come from the embedder)
    sample_embedding = [0.1] * 384  # Placeholder embedding

    # Store a sample chunk
    sample_chunk_id = str(uuid.uuid4())
    vector_store.store_chunk(
        chunk_id=sample_chunk_id,
        embedding=sample_embedding,
        content="This is a sample content chunk for testing.",
        metadata={"chapter_id": "chapter_1", "section": "introduction"}
    )

    # Search for similar content
    search_results = vector_store.search_similar(sample_embedding, limit=1)
    print(f"Search results: {search_results}")