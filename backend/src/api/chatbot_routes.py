from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import logging
from uuid import UUID
import os
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.question import QuestionRequest, QuestionResponse, Citation
from ..models.question import Question as QuestionModel, QuestionCreate
from ..models.answer import AnswerCreate
from ..services.rag_service import RAGService
from ..db import get_db, Question as DBQuestion, Answer as DBAnswer
from ..auth import get_current_active_user
from ..models.user import User
from ..exceptions import ValidationError, DatabaseError, BusinessLogicError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chatbot", tags=["chatbot"])

def get_rag_service():
    """
    Dependency to create and get a RAGService instance.
    """
    from ai_pipeline.src.embedding.embedder import Embedder
    from ai_pipeline.src.rag.vector_store import VectorStore
    from ai_pipeline.src.rag.claude_processor import ClaudeProcessor
    
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


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    current_user: User = Depends(get_current_active_user),
    rag_service = Depends(get_rag_service),
    db: Session = Depends(get_db)
):
    """
    Submit a question about textbook content and receive an answer with citations
    """
    if not request.question or not request.question.strip():
        raise ValidationError("Question cannot be empty")

    try:
        # Create a question record in the database
        from uuid import uuid4
        question_id = uuid4()
        
        db_question = DBQuestion(
            id=question_id,
            user_id=current_user.id,
            question_text=request.question,
            chapter_context_id=request.chapter_id,
            status='pending'
        )
        
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        # Process the query through the RAG pipeline
        result = rag_service.process_query(
            query=request.question,
            user_id=str(current_user.id),
            chapter_context=request.chapter_id
        )

        # Create an answer record in the database
        answer_id = uuid4()
        
        # Convert citations to JSON string for storage
        import json
        citations_json = json.dumps([citation.dict() for citation in result["citations"]])
        
        db_answer = DBAnswer(
            id=answer_id,
            question_id=question_id,
            answer_text=result["answer"],
            citations=citations_json,
            confidence_score=int(result["confidence_score"] * 100)  # Store as integer 0-100
        )
        
        db.add(db_answer)
        db.commit()

        # Update question status to processed
        db_question.status = 'processed'
        db.commit()

        # Format the response
        response = QuestionResponse(
            id=str(question_id),
            question=request.question,
            answer=result["answer"],
            citations=result["citations"] if request.include_citations else [],
            confidence_score=result["confidence_score"],
            created_at=datetime.utcnow().isoformat(),
        )

        logger.info(f"Question answered successfully for query: {request.question[:50]}...")
        return response

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise BusinessLogicError(detail="Error processing your question")


@router.get("/history")
async def get_question_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve the history of questions asked by the authenticated user
    """
    from sqlalchemy import desc
    import json
    
    logger.info(f"Retrieving question history for user: {current_user.id}")

    try:
        # Query questions and answers from the database
        db_questions = db.query(DBQuestion).filter(
            DBQuestion.user_id == current_user.id
        ).order_by(desc(DBQuestion.created_at)).limit(10).all()

        history = []
        for db_question in db_questions:
            # Get the corresponding answer
            db_answer = db.query(DBAnswer).filter(DBAnswer.question_id == db_question.id).first()
            
            # Parse citations from JSON string
            citations = []
            if db_answer and db_answer.citations:
                try:
                    citations_list = json.loads(db_answer.citations)
                    citations = [Citation(**item) for item in citations_list]
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse citations for answer {db_answer.id if db_answer else 'None'}")
            
            question_response = QuestionResponse(
                id=str(db_question.id),
                question=db_question.question_text,
                answer=db_answer.answer_text if db_answer else "",
                citations=citations,
                confidence_score=db_answer.confidence_score / 100.0 if db_answer and db_answer.confidence_score else 0.0,
                created_at=db_question.created_at.isoformat() if db_question.created_at else datetime.utcnow().isoformat(),
            )
            
            history.append(question_response)

        logger.info(f"Retrieved {len(history)} questions from history")
        return history
    except Exception as e:
        logger.error(f"Error retrieving question history: {str(e)}", exc_info=True)
        raise DatabaseError(detail="Failed to retrieve question history due to database error")


# Additional utility endpoint for testing
@router.post("/test-rag")
async def test_rag_pipeline(rag_service = Depends(get_rag_service)):
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
        logger.error(f"Error in RAG test: {str(e)}", exc_info=True)
        raise BusinessLogicError(detail=f"RAG pipeline test failed: {str(e)}")