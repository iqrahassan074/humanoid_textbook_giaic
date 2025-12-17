from fastapi import APIRouter, HTTPException, status
from typing import List
import logging
from uuid import UUID

# Import models and services - using dict as placeholder since we don't have full DB implementation
from ..models.content_chunk import ContentChunk

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chapters", tags=["chapters"])

# In a real implementation, these would come from a database
# For now, using placeholder data to demonstrate the API structure
CHAPTERS_DATA = [
    {
        "id": "1",
        "title": "Introduction to Physical AI",
        "number": 1,
        "content": "This is the content for Chapter 1: Introduction to Physical AI...",
        "is_published": True,
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    },
    {
        "id": "2",
        "title": "Robotics and AI Integration",
        "number": 2,
        "content": "This is the content for Chapter 2: Robotics and AI Integration...",
        "is_published": True,
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    },
    {
        "id": "3",
        "title": "Sensorimotor Learning",
        "number": 3,
        "content": "This is the content for Chapter 3: Sensorimotor Learning...",
        "is_published": True,
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    },
    {
        "id": "4",
        "title": "Human-Robot Interaction",
        "number": 4,
        "content": "This is the content for Chapter 4: Human-Robot Interaction...",
        "is_published": True,
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    },
    {
        "id": "5",
        "title": "Embodied Intelligence",
        "number": 5,
        "content": "This is the content for Chapter 5: Embodied Intelligence...",
        "is_published": True,
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    },
    {
        "id": "6",
        "title": "Future of Physical AI",
        "number": 6,
        "content": "This is the content for Chapter 6: Future of Physical AI...",
        "is_published": True,
        "created_at": "2025-12-15T00:00:00Z",
        "updated_at": "2025-12-15T00:00:00Z"
    }
]

@router.get("/", response_model=List[dict])
async def get_all_chapters():
    """
    Retrieve a list of all available textbook chapters
    """
    logger.info("Retrieving all chapters")

    # Filter only published chapters
    published_chapters = [chap for chap in CHAPTERS_DATA if chap["is_published"]]

    # Sort by chapter number
    sorted_chapters = sorted(published_chapters, key=lambda x: x["number"])

    return sorted_chapters


@router.get("/{chapter_id}", response_model=dict)
async def get_chapter(chapter_id: str):
    """
    Retrieve a specific textbook chapter by ID
    """
    logger.info(f"Retrieving chapter with ID: {chapter_id}")

    # Find chapter by ID
    chapter = None
    for chap in CHAPTERS_DATA:
        if chap["id"] == chapter_id or str(chap["number"]) == chapter_id:
            chapter = chap
            break

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    if not chapter["is_published"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    return chapter


# Additional utility endpoint for content management (would require auth in real implementation)
@router.post("/index-content")
async def index_chapter_content(chapter_data: dict):
    """
    Index chapter content for the RAG system
    """
    from .chatbot_routes import rag_service  # Import here to avoid circular dependency

    chapter_id = chapter_data.get("chapter_id")
    content = chapter_data.get("content")

    if not chapter_id or not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="chapter_id and content are required"
        )

    try:
        # Use the RAG service to index the content
        result = rag_service.index_content(chapter_id, content)
        logger.info(f"Successfully indexed content for chapter {chapter_id}")
        return result
    except Exception as e:
        logger.error(f"Error indexing content for chapter {chapter_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error indexing chapter content: {str(e)}"
        )