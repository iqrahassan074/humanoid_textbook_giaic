from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import UUID, uuid4


class ContentChunk(BaseModel):
    """
    Represents a chunk of textbook content for vector search in the RAG pipeline
    """
    id: UUID
    chapter_id: UUID
    content: str
    embedding_vector: Optional[list] = None  # Vector representation for similarity search
    chunk_metadata: Optional[dict] = None  # Additional metadata
    created_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class ContentChunkCreate(BaseModel):
    """
    Schema for creating a new content chunk
    """
    chapter_id: UUID
    content: str
    chunk_metadata: Optional[dict] = None


class ContentChunkUpdate(BaseModel):
    """
    Schema for updating a content chunk
    """
    content: Optional[str] = None
    chunk_metadata: Optional[dict] = None