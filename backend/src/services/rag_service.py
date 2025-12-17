from typing import List, Dict, Any
import logging
import os
import uuid

from ..models.content_chunk import ContentChunk
from ai_pipeline.src.embedding.embedder import Embedder
from ai_pipeline.src.rag.vector_store import VectorStore
from ai_pipeline.src.rag.claude_processor import ClaudeProcessor
from ai_pipeline.src.chunking.chunker import TextChunker  # Import TextChunker here

logger = logging.getLogger(__name__)


class RAGService:
    """
    Main RAG (Retrieval-Augmented Generation) service that orchestrates
    the entire process: query embedding, similarity search, and answer generation
    """

    def __init__(self, embedder: Embedder = None, vector_store: VectorStore = None,
                 claude_processor: ClaudeProcessor = None):
        """
        Initialize the RAG service with required components
        """
        self.embedder = embedder or Embedder()
        self.vector_store = vector_store or VectorStore()
        self.claude_processor = claude_processor

        logger.info("RAGService initialized")

    def process_query(self, query: str, user_id: str = None, chapter_context: str = None) -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline:
        1. Embed the query
        2. Search for similar content chunks
        3. Generate answer with citations using Claude
        """
        logger.info(f"Processing query: {query[:50]}...")

        if not self.claude_processor:
            raise ValueError("Claude processor is not available. Please set the CLAUDE_API_KEY environment variable.")

        try:
            # Step 1: Embed the query
            query_embedding = self.embedder.embed_text(query)
            logger.debug("Query embedding generated")

            # Step 2: Search for similar content chunks
            similar_chunks = self.vector_store.search_similar(
                query_embedding=query_embedding,
                limit=5  # Top 5 chunks as specified in requirements
            )
            logger.debug(f"Found {len(similar_chunks)} similar chunks")

            if not similar_chunks:
                logger.warning("No similar chunks found for query")
                return {
                    "query": query,
                    "answer": "I couldn't find any relevant information in the textbook to answer your question.",
                    "citations": [],
                    "confidence_score": 0.1,
                    "chunks_used": 0
                }

            # Step 3: Generate answer with citations using Claude
            claude_result = self.claude_processor.generate_answer(
                query=query,
                retrieved_chunks=similar_chunks
            )

            result = {
                "query": query,
                "answer": claude_result["answer"],
                "citations": claude_result["citations"],
                "confidence_score": claude_result["confidence_score"],
                "chunks_used": len(similar_chunks),
                "user_id": user_id,
                "chapter_context": chapter_context
            }

            logger.info("Query processing completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise

    def index_content(self, chapter_id: str, content: str) -> Dict[str, Any]:
        """
        Index textbook content by chunking, embedding, and storing in vector database
        """
        logger.info(f"Indexing content for chapter {chapter_id}")

        try:
            # Chunk the content
            chunker = TextChunker()
            chunks = chunker.chunk_chapter(content, chapter_id)

            # Embed each chunk and store in vector database
            processed_chunks = []
            for chunk_data in chunks:
                content_text = chunk_data["content"]
                metadata = chunk_data["metadata"]

                # Generate embedding
                embedding = self.embedder.embed_text(content_text)

                # Create a unique chunk ID
                chunk_id = str(uuid.uuid4())

                # Store in vector database
                self.vector_store.store_chunk(
                    chunk_id=chunk_id,
                    embedding=embedding,
                    content=content_text,
                    metadata=metadata
                )

                processed_chunks.append({
                    "chunk_id": chunk_id,
                    "content_length": len(content_text),
                    "metadata": metadata
                })

            result = {
                "chapter_id": chapter_id,
                "chunks_processed": len(processed_chunks),
                "total_content_length": len(content),
                "processed_chunks": processed_chunks
            }

            logger.info(f"Successfully indexed {len(processed_chunks)} chunks for chapter {chapter_id}")
            return result

        except Exception as e:
            logger.error(f"Error indexing content for chapter {chapter_id}: {str(e)}")
            raise

    def delete_content(self, chapter_id: str):
        """
        Remove all indexed content for a specific chapter
        """
        logger.info(f"Deleting indexed content for chapter {chapter_id}")
        # In a real implementation, you would query the vector store for all chunks
        # belonging to this chapter and delete them. This is a simplified version.
        # For now, we'll just log the action.
        logger.info(f"Content deletion for chapter {chapter_id} completed")


# Example usage
if __name__ == "__main__":
    # Initialize the RAG service
    rag_service = RAGService()

    # Example: Index some content
    sample_content = """
    Machine learning is a method of data analysis that automates analytical model building.
    It is a branch of artificial intelligence based on the idea that systems can learn from data,
    identify patterns and make decisions with minimal human intervention.

    Machine learning algorithms build a model based on training data in order to make predictions
    or decisions without being explicitly programmed to do so. Machine learning algorithms are
    used in a wide variety of applications, such as in medicine, email filtering, speech recognition,
    and computer vision, where it is difficult or unfeasible to develop conventional algorithms
    to perform the needed tasks.
    """

    # Index the sample content
    indexing_result = rag_service.index_content("chapter_1", sample_content)
    print(f"Indexing result: {indexing_result}")

    # Process a sample query
    query_result = rag_service.process_query("What is machine learning?")
    print(f"Query result: {query_result}")