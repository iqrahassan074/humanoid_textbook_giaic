from typing import List, Dict, Any, Optional
import logging
from uuid import UUID
from datetime import datetime

from ..models.question import Question, QuestionCreate, QuestionUpdate, QuestionStatus
from ..models.answer import Answer, AnswerCreate
from .rag_service import RAGService

logger = logging.getLogger(__name__)


class QuestionService:
    """
    Service for managing questions and their processing lifecycle
    """

    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        logger.info("QuestionService initialized")

    def create_question(self, question_data: QuestionCreate) -> Question:
        """
        Create a new question record
        """
        from uuid import uuid4
        question = Question(
            id=uuid4(),
            user_id=question_data.user_id,
            question_text=question_data.question_text,
            chapter_context_id=question_data.chapter_context_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            status=QuestionStatus.PENDING
        )
        logger.info(f"Created question {question.id} for user {question.user_id}")
        return question

    def process_question(self, question: Question) -> Dict[str, Any]:
        """
        Process a question through the RAG pipeline and return the result
        """
        logger.info(f"Processing question {question.id}: {question.question_text[:50]}...")

        try:
            # Update question status to processing
            question.status = QuestionStatus.PROCESSED

            # Process through RAG service
            rag_result = self.rag_service.process_query(
                query=question.question_text,
                user_id=str(question.user_id),
                chapter_context=question.chapter_context_id
            )

            # Create response with the RAG result
            result = {
                "question": question,
                "answer": rag_result["answer"],
                "citations": rag_result["citations"],
                "confidence_score": rag_result["confidence_score"],
                "status": QuestionStatus.PROCESSED
            }

            logger.info(f"Successfully processed question {question.id}")
            return result

        except Exception as e:
            logger.error(f"Error processing question {question.id}: {str(e)}")
            question.status = QuestionStatus.ERROR
            raise

    def get_question_history(self, user_id: UUID, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get question history for a specific user (in a real app, this would query a database)
        """
        # In a real implementation, this would fetch from a database
        # For now, return an empty list or sample data
        logger.info(f"Retrieving question history for user {user_id}")
        return []

    def validate_question(self, question_text: str) -> bool:
        """
        Validate if a question is appropriate for the system
        """
        if not question_text or len(question_text.strip()) < 3:
            return False

        # Additional validation could be added here
        return True


# Example usage
if __name__ == "__main__":
    # This would be used in conjunction with the RAG service
    pass