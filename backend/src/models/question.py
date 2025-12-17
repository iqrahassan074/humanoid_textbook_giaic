from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import UUID, uuid4


class QuestionStatus:
    PENDING = "pending"
    PROCESSED = "processed"
    ERROR = "error"


class Question(BaseModel):
    """
    Represents a user's query submitted to the chatbot with timestamp and context
    """
    id: UUID
    user_id: UUID  # Foreign key to User
    question_text: str
    chapter_context_id: Optional[UUID] = None  # Optional chapter ID for context
    created_at: datetime
    updated_at: datetime
    status: str = QuestionStatus.PENDING  # pending, processed, error

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class QuestionCreate(BaseModel):
    """
    Schema for creating a new question
    """
    user_id: UUID
    question_text: str
    chapter_context_id: Optional[UUID] = None


class QuestionUpdate(BaseModel):
    """
    Schema for updating a question
    """
    question_text: Optional[str] = None
    status: Optional[str] = None
    chapter_context_id: Optional[UUID] = None


class QuestionResponse(BaseModel):
    """
    Schema for question response with answer
    """
    question: Question
    answer_text: Optional[str] = None
    citations: Optional[list] = None
    confidence_score: Optional[float] = None