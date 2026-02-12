from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from uuid import UUID


class ChapterBase(BaseModel):
    title: str
    number: int  # 1-6 for textbook chapters
    content: str
    is_published: bool = True
    metadata: Optional[Dict[str, Any]] = None


class ChapterCreate(ChapterBase):
    """
    Schema for creating a new chapter
    """
    pass


class ChapterUpdate(BaseModel):
    """
    Schema for updating a chapter
    """
    title: Optional[str] = None
    number: Optional[int] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class Chapter(ChapterBase):
    """
    Represents one of the 6 textbook chapters with content, metadata, and citation information
    """
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        # Allow UUID serialization
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True  # Enable ORM mode