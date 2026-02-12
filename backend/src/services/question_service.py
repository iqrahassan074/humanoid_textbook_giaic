from typing import List, Dict, Any, Optional
import logging
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.question import Question, QuestionCreate, QuestionUpdate, QuestionStatus
from ..models.answer import Answer, AnswerCreate, Citation
from .rag_service import RAGService
from ..db import Question as DBQuestion, Answer as DBAnswer

logger = logging.getLogger(__name__)


class QuestionService:
    """
    Service for managing questions and their processing lifecycle
    """

    def __init__(self, rag_service: RAGService, db_session: Session):
        self.rag_service = rag_service
        self.db = db_session
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
        Get question history for a specific user
        """
        from sqlalchemy import desc
        import json
        
        logger.info(f"Retrieving question history for user {user_id}")
        
        # Query questions from the database
        db_questions = self.db.query(DBQuestion).filter(
            DBQuestion.user_id == user_id
        ).order_by(desc(DBQuestion.created_at)).limit(limit).all()

        history = []
        for db_question in db_questions:
            # Get the corresponding answer
            db_answer = self.db.query(DBAnswer).filter(DBAnswer.question_id == db_question.id).first()
            
            # Parse citations from JSON string
            citations = []
            if db_answer and db_answer.citations:
                try:
                    citations_list = json.loads(db_answer.citations)
                    citations = [Citation(**item) for item in citations_list]
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse citations for answer {db_answer.id if db_answer else 'None'}")
            
            question_dict = {
                "id": str(db_question.id),
                "question_text": db_question.question_text,
                "answer_text": db_answer.answer_text if db_answer else "",
                "citations": citations,
                "confidence_score": db_answer.confidence_score / 100.0 if db_answer and db_answer.confidence_score else 0.0,
                "created_at": db_question.created_at.isoformat() if db_question.created_at else datetime.utcnow().isoformat(),
            }
            
            history.append(question_dict)

        logger.info(f"Retrieved {len(history)} questions from history")
        return history

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