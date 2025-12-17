from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any
import logging
from uuid import UUID
import os
from pydantic import BaseModel
from datetime import datetime

from ..models.content_chunk import ContentChunk
from ..services.rag_service import RAGService
from ai_pipeline.src.embedding.embedder import Embedder
from ai_pipeline.src.rag.vector_store import VectorStore
from ai_pipeline.src.rag.claude_processor import ClaudeProcessor

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chatbot", tags=["chatbot"])

def get_rag_service():
    """
    Dependency to create and get a RAGService instance.
    """
    embedder = Embedder()
    vector_store = VectorStore()
    claude_processor = None
    if os.getenv("CLAUDE_API_KEY"):
        try:
            claude_processor = ClaudeProcessor()
        except ValueError as e:
            logger.warning(f"Could not initialize Claude processor: {e}")
    
    rag_service = RAGService(
        embedder=embedder,
        vector_store=vector_store,
        claude_processor=claude_processor
    )
    return rag_service


class QuestionRequest(BaseModel):
    question: str
    chapter_id: str = None
    include_citations: bool = True


class QuestionResponse(BaseModel):
    id: str
    question: str
    answer: str
    citations: List[Dict]
    confidence_score: float
    created_at: str


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    rag_service: RAGService = Depends(get_rag_service)
    # current_user: User = Depends(get_current_user)  # Assuming authentication is implemented
):
    """
    Submit a question about textbook content and receive an answer with citations
    """
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty"
        )

    try:
        # Process the query through the RAG pipeline
        result = rag_service.process_query(
            query=request.question,
            # user_id=current_user.id,  # Uncomment when authentication is implemented
            chapter_context=request.chapter_id
        )

        # Generate a response ID
        import uuid
        response_id = str(uuid.uuid4())

        # Format the response
        response = QuestionResponse(
            id=response_id,
            question=request.question,
            answer=result["answer"],
            citations=result["citations"] if request.include_citations else [],
            confidence_score=result["confidence_score"],
            created_at=datetime.utcnow().isoformat(),
        )

        logger.info(f"Question answered successfully for query: {request.question[:50]}...")
        return response

    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your question"
        )


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_question_history(
    # current_user: User = Depends(get_current_user)  # Assuming authentication is implemented
):
    """
    Retrieve the history of questions asked by the authenticated user
    """
    # In a real implementation, this would fetch from a database
    # For now, return an empty list
    logger.info("Retrieved question history")
    return []


# Additional utility endpoint for testing
@router.post("/test-rag")
async def test_rag_pipeline(rag_service: RAGService = Depends(get_rag_service)):
    """
    Test endpoint to verify the RAG pipeline is working
    """
    try:
        # Test with a simple query
        result = rag_service.process_query("What is this system?")
        return {
            "status": "success",
            "message": "RAG pipeline is working",
            "test_result": result
        }
    except Exception as e:
        logger.error(f"Error in RAG test: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG pipeline test failed: {str(e)}"
        )


# Dependency to get current user (to be implemented with auth)
def get_current_user():
    # This is a placeholder - implement actual authentication
    # This would typically decode JWT and return user info
    pass