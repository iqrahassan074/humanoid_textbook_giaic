from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID


class ContentChunkBase(BaseModel):
    chapter_id: UUID
    content: str
    chunk_metadata: Optional[Dict[str, Any]] = None


class ContentChunkCreate(ContentChunkBase):
    """
    Schema for creating a new content chunk
    """
    chapter_id: UUID
    content: str
    chunk_metadata: Optional[Dict[str, Any]] = None


class ContentChunkUpdate(BaseModel):
    """
    Schema for updating a content chunk
    """
    content: Optional[str] = None
    chunk_metadata: Optional[Dict[str, Any]] = None


class ContentChunk(ContentChunkBase):
    """
    Represents a chunk of textbook content for vector search in the RAG pipeline
    """
    id: UUID
    embedding_vector: Optional[list] = None  # Vector representation for similarity search
    created_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True  # Enable ORM mode