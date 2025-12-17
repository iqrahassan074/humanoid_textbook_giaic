from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from uuid import UUID, uuid4


class Answer(BaseModel):
    """
    Represents the chatbot's response with citations to source material and confidence level
    """
    id: UUID
    question_id: UUID  # Foreign key to Question (unique relationship)
    answer_text: str
    citations: List[Dict[str, Any]]  # Source references (JSON array)
    confidence_score: float  # 0.0-1.0
    created_at: datetime
    updated_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class AnswerCreate(BaseModel):
    """
    Schema for creating a new answer
    """
    question_id: UUID
    answer_text: str
    citations: List[Dict[str, Any]]
    confidence_score: float


class AnswerUpdate(BaseModel):
    """
    Schema for updating an answer
    """
    answer_text: Optional[str] = None
    citations: Optional[List[Dict[str, Any]]] = None
    confidence_score: Optional[float] = None


class Citation(BaseModel):
    """
    Represents a citation in the answer
    """
    source: str  # The specific source text or section
    chapter: str  # Chapter where the citation is found
    page_reference: str  # Page or section reference
    content_preview: Optional[str] = None  # Preview of the cited content