from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from uuid import UUID


class QuestionStatus:
    PENDING = "pending"
    PROCESSED = "processed"
    ERROR = "error"


class QuestionBase(BaseModel):
    question_text: str
    chapter_context_id: Optional[UUID] = None
    status: str = QuestionStatus.PENDING


class QuestionCreate(QuestionBase):
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


class Question(QuestionBase):
    """
    Represents a user's query submitted to the chatbot with timestamp and context
    """
    id: UUID
    user_id: UUID  # Foreign key to User
    created_at: datetime
    updated_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True  # Enable ORM mode


class Citation(BaseModel):
    """
    Represents a citation in the answer
    """
    source: str  # The specific source text or section
    chapter: str  # Chapter where the citation is found
    page_reference: str  # Page or section reference
    content_preview: Optional[str] = None  # Preview of the cited content


class AnswerBase(BaseModel):
    answer_text: str
    citations: List[Citation]  # Source references (JSON array)
    confidence_score: float  # 0.0-1.0


class AnswerCreate(AnswerBase):
    """
    Schema for creating a new answer
    """
    question_id: UUID
    answer_text: str
    citations: List[Citation]
    confidence_score: float


class AnswerUpdate(BaseModel):
    """
    Schema for updating an answer
    """
    answer_text: Optional[str] = None
    citations: Optional[List[Citation]] = None
    confidence_score: Optional[float] = None


class Answer(AnswerBase):
    """
    Represents the chatbot's response with citations to source material and confidence level
    """
    id: UUID
    question_id: UUID  # Foreign key to Question (unique relationship)
    created_at: datetime
    updated_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True  # Enable ORM mode


class QuestionRequest(BaseModel):
    """
    Request model for asking a question to the chatbot
    """
    question: str
    chapter_id: Optional[str] = None
    include_citations: bool = True


class QuestionResponse(BaseModel):
    """
    Response model for a question asked to the chatbot
    """
    id: str
    question: str
    answer: str
    citations: List[Citation]
    confidence_score: float
    created_at: str