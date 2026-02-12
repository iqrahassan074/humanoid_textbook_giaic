from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union, Optional
import logging

logger = logging.getLogger(__name__)


class Embedder:
    """
    Handles text embedding generation using sentence-transformers
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedder with a pre-trained model
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        logger.info(f"Embedder configured with model: {model_name}")

    def _get_model(self) -> SentenceTransformer:
        """
        Get the SentenceTransformer model, creating it if it doesn't exist
        """
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        return self.model

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            embedding = self._get_model().encode([text])
            return embedding[0].tolist()  # Convert to list for JSON serialization
        except Exception as e:
            logger.error(f"Error embedding text: {str(e)}")
            raise

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        """
        try:
            embeddings = self._get_model().encode(texts)
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            logger.error(f"Error embedding texts: {str(e)}")
            raise

    def compute_similarity(self, query_embedding: List[float],
                          chunk_embedding: List[float]) -> float:
        """
        Compute cosine similarity between query and chunk embeddings
        """
        query_array = np.array(query_embedding)
        chunk_array = np.array(chunk_embedding)

        # Compute cosine similarity
        cosine_similarity = np.dot(query_array, chunk_array) / (
            np.linalg.norm(query_array) * np.linalg.norm(chunk_array)
        )

        return float(cosine_similarity)


# Example usage
if __name__ == "__main__":
    embedder = Embedder()

    # Example texts
    texts = [
        "This is the first chunk of content about machine learning.",
        "This is another chunk about deep learning techniques.",
        "Here's a third chunk discussing neural networks."
    ]

    # Generate embeddings
    embeddings = embedder.embed_texts(texts)
    print(f"Generated {len(embeddings)} embeddings")

    # Example similarity calculation
    query_embedding = embedder.embed_text("What is machine learning?")
    similarity = embedder.compute_similarity(query_embedding, embeddings[0])
    print(f"Similarity: {similarity}")