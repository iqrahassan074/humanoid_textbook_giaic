import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Handles chunking of textbook content into smaller pieces for RAG processing
    """

    def __init__(self, max_chunk_size: int = 512, overlap: int = 50):
        """
        Initialize the chunker with configuration
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        logger.info(f"TextChunker initialized with max_chunk_size: {max_chunk_size}, overlap: {overlap}")

    def chunk_text(self, text: str, chapter_id: str = None) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks
        """
        # Split text by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        chunk_id = 0

        for paragraph in paragraphs:
            # If paragraph is smaller than max chunk size, use as is
            if len(paragraph) <= self.max_chunk_size:
                chunk_metadata = {
                    "chunk_id": chunk_id,
                    "chapter_id": chapter_id,
                    "type": "paragraph",
                    "original_length": len(paragraph)
                }
                chunks.append({
                    "content": paragraph,
                    "metadata": chunk_metadata
                })
                chunk_id += 1
            else:
                # Split large paragraph into smaller chunks
                sub_chunks = self._split_large_text(paragraph)
                for sub_chunk in sub_chunks:
                    chunk_metadata = {
                        "chunk_id": chunk_id,
                        "chapter_id": chapter_id,
                        "type": "sub_chunk",
                        "original_length": len(paragraph)
                    }
                    chunks.append({
                        "content": sub_chunk,
                        "metadata": chunk_metadata
                    })
                    chunk_id += 1

        return chunks

    def _split_large_text(self, text: str) -> List[str]:
        """
        Split large text into overlapping chunks
        """
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = []
        current_chunk = ""
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence would exceed the limit
            if current_length + len(sentence) > self.max_chunk_size and current_chunk:
                # Save the current chunk
                chunks.append(current_chunk.strip())

                # Start a new chunk with overlap
                if self.overlap > 0:
                    # Get the end of the current chunk as overlap
                    overlap_start = max(0, len(current_chunk) - self.overlap)
                    current_chunk = current_chunk[overlap_start:] + " " + sentence
                    current_length = len(current_chunk)
                else:
                    current_chunk = sentence
                    current_length = len(sentence)
            else:
                current_chunk += " " + sentence if current_chunk else sentence
                current_length += len(sentence) + (1 if current_chunk != sentence else 0)

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def chunk_chapter(self, chapter_content: str, chapter_id: str) -> List[Dict[str, Any]]:
        """
        Process an entire chapter and return chunks with metadata
        """
        logger.info(f"Chunking chapter {chapter_id} of length {len(chapter_content)}")

        raw_chunks = self.chunk_text(chapter_content, chapter_id)

        processed_chunks = []
        for i, chunk_data in enumerate(raw_chunks):
            processed_chunk = {
                "content": chunk_data["content"],
                "metadata": {
                    **chunk_data["metadata"],
                    "section_number": i + 1,
                    "total_chunks": len(raw_chunks)
                }
            }
            processed_chunks.append(processed_chunk)

        logger.info(f"Generated {len(processed_chunks)} chunks for chapter {chapter_id}")
        return processed_chunks


# Example usage
if __name__ == "__main__":
    chunker = TextChunker(max_chunk_size=200, overlap=30)

    sample_text = """
    Machine learning is a method of data analysis that automates analytical model building.
    It is a branch of artificial intelligence based on the idea that systems can learn from data,
    identify patterns and make decisions with minimal human intervention.

    Machine learning algorithms build a model based on training data in order to make predictions
    or decisions without being explicitly programmed to do so. Machine learning algorithms are
    used in a wide variety of applications, such as in medicine, email filtering, speech recognition,
    and computer vision, where it is difficult or unfeasible to develop conventional algorithms
    to perform the needed tasks.

    Deep learning is part of a broader family of machine learning methods based on artificial neural
    networks with representation learning. Learning can be supervised, semi-supervised or unsupervised.
    """

    chunks = chunker.chunk_text(sample_text, "chapter_1")
    print(f"Generated {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {len(chunk['content'])} chars - {chunk['content'][:50]}...")