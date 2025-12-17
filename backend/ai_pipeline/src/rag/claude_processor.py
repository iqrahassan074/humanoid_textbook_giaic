import os
import json
from typing import List, Dict, Any, Optional
import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeProcessor:
    """
    Handles processing of retrieved chunks through Claude to generate answers with citations
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Claude processor with API key
        """
        self.api_key = api_key
        self.client: Optional[Anthropic] = None
        logger.info("ClaudeProcessor configured")

    def _get_client(self) -> Anthropic:
        """
        Get the Anthropic client, creating it if it doesn't exist
        """
        if self.client is None:
            api_key = self.api_key or os.getenv("CLAUDE_API_KEY")
            if not api_key:
                raise ValueError("CLAUDE_API_KEY environment variable must be set")
            self.client = Anthropic(api_key=api_key)
        return self.client

    def generate_answer(self, query: str, retrieved_chunks: List[Dict[str, Any]],
                       max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Generate an answer to the query based on retrieved chunks, with citations
        """
        # Format the context from retrieved chunks
        context = self._format_context(retrieved_chunks)

        # Create the prompt for Claude
        prompt = self._create_prompt(query, context)

        try:
            # Call Claude API to generate response
            response = self._get_client().messages.create(
                model="claude-3-haiku-20240307",  # or another Claude model
                max_tokens=max_tokens,
                temperature=0.3,
                system="You are an AI assistant that answers questions based only on the provided context. Only use information from the context. If the answer is not in the context, say so. Always provide citations to the specific chapters and sections where you found the information.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the answer text
            answer_text = response.content[0].text if response.content else ""

            # Extract citations from the response
            citations = self._extract_citations(answer_text, retrieved_chunks)

            # Calculate confidence score based on response quality
            confidence_score = self._calculate_confidence(answer_text, retrieved_chunks)

            result = {
                "answer": answer_text,
                "citations": citations,
                "confidence_score": confidence_score,
                "model": response.model,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }

            logger.debug(f"Generated answer with {len(citations)} citations")
            return result

        except Exception as e:
            logger.error(f"Error generating answer with Claude: {str(e)}")
            raise

    def _format_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Format the retrieved chunks into a context string for Claude
        """
        formatted_chunks = []
        for i, chunk in enumerate(retrieved_chunks):
            content = chunk.get("content", "")
            metadata = chunk.get("metadata", {})
            chunk_id = chunk.get("id", f"chunk_{i}")

            formatted_chunk = f"""
            [SOURCE {i+1}]:
            Content: {content}
            Chapter ID: {metadata.get('chapter_id', 'Unknown')}
            Section: {metadata.get('section_number', 'Unknown')}
            Similarity Score: {chunk.get('similarity_score', 0.0):.3f}
            Chunk ID: {chunk_id}
            ---
            """
            formatted_chunks.append(formatted_chunk)

        return "\n".join(formatted_chunks)

    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create the prompt for Claude with query and context
        """
        prompt = f"""
        CONTEXT:
        {context}

        QUESTION:
        {query}

        INSTRUCTIONS:
        1. Answer the question based ONLY on the provided context
        2. If the answer is not in the context, clearly state that the information is not available in the provided content
        3. Provide specific citations to the sources you used (mention source numbers, chapter IDs, and section numbers)
        4. Be concise but comprehensive in your answer
        5. Maintain academic tone appropriate for educational content

        RESPONSE FORMAT:
        First provide the answer to the question.
        Then list the citations in the format:
        Citations:
        - Source [number]: Chapter [ID], Section [number]
        - Source [number]: Chapter [ID], Section [number]
        """
        return prompt

    def _extract_citations(self, answer_text: str, retrieved_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract citation information from the answer text
        """
        citations = []

        # Look for source references in the answer (e.g., "Source 1", "Source 2", etc.)
        for i, chunk in enumerate(retrieved_chunks):
            # Check if this chunk's information was used (simple heuristic)
            # In a real implementation, you might use more sophisticated NLP to detect usage
            chunk_metadata = chunk.get("metadata", {})

            citation = {
                "source_number": i + 1,
                "chapter": chunk_metadata.get("chapter_id", "Unknown"),
                "section": chunk_metadata.get("section_number", "Unknown"),
                "similarity_score": chunk.get("similarity_score", 0.0),
                "content_preview": chunk.get("content", "")[:200] + "..." if len(chunk.get("content", "")) > 200 else chunk.get("content", ""),
                "chunk_id": chunk.get("id", f"chunk_{i}")
            }
            citations.append(citation)

        return citations

    def _calculate_confidence(self, answer_text: str, retrieved_chunks: List[Dict[str, Any]]) -> float:
        """
        Calculate a confidence score based on various factors
        """
        if not answer_text or "not available" in answer_text.lower() or "not found" in answer_text.lower():
            return 0.1  # Low confidence if answer indicates info not available

        # Calculate confidence based on number of chunks used and their similarity scores
        if retrieved_chunks:
            avg_similarity = sum(
                chunk.get("similarity_score", 0.0) for chunk in retrieved_chunks
            ) / len(retrieved_chunks)

            # Adjust based on answer length (longer answers might be more complete)
            length_factor = min(len(answer_text) / 200, 1.0)  # Cap at 1.0

            confidence = (avg_similarity * 0.7) + (length_factor * 0.3)
            return min(confidence, 1.0)  # Cap at 1.0
        else:
            return 0.2  # Low confidence if no chunks were retrieved


# Example usage
if __name__ == "__main__":
    import os
    # This example would require a valid Claude API key
    # api_key = os.getenv("CLAUDE_API_KEY")
    # if api_key:
    #     processor = ClaudeProcessor(api_key=api_key)
    #
    #     sample_query = "What is machine learning?"
    #     sample_chunks = [
    #         {
    #             "id": "chunk_1",
    #             "content": "Machine learning is a method of data analysis that automates analytical model building.",
    #             "metadata": {"chapter_id": "chapter_1", "section_number": 1},
    #             "similarity_score": 0.85
    #         },
    #         {
    #             "id": "chunk_2",
    #             "content": "It is a branch of artificial intelligence based on the idea that systems can learn from data.",
    #             "metadata": {"chapter_id": "chapter_1", "section_number": 2},
    #             "similarity_score": 0.78
    #         }
    #     ]
    #
    #     result = processor.generate_answer(sample_query, sample_chunks)
    #     print(f"Answer: {result['answer']}")
    #     print(f"Citations: {result['citations']}")
    #     print(f"Confidence: {result['confidence_score']}")
    # else:
    #     print("CLAUDE_API_KEY not set, skipping Claude API call example")