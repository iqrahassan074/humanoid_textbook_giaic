from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import logging
from uuid import UUID
from sqlalchemy.orm import Session

# Import models and services
from ..models.chapter import Chapter
from ..db import get_db, Chapter as DBChapter
from ..exceptions import ResourceNotFoundError, DatabaseError, ValidationError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.get("/", response_model=List[Chapter])
async def get_all_chapters(db: Session = Depends(get_db)):
    """
    Retrieve a list of all available textbook chapters
    """
    logger.info("Retrieving all chapters")

    try:
        # Query published chapters from database
        chapters = db.query(DBChapter).filter(DBChapter.is_published == True).order_by(DBChapter.number).all()

        # Convert DB chapters to Pydantic chapters
        chapters_response = []
        for db_chapter in chapters:
            chapter_response = Chapter(
                id=db_chapter.id,
                title=db_chapter.title,
                number=db_chapter.number,
                content=db_chapter.content,
                is_published=db_chapter.is_published,
                metadata=db_chapter.metadata_json,
                created_at=db_chapter.created_at,
                updated_at=db_chapter.updated_at or db_chapter.created_at
            )
            chapters_response.append(chapter_response)

        return chapters_response
    except Exception as e:
        logger.error(f"Error retrieving chapters: {str(e)}", exc_info=True)
        raise DatabaseError(detail="Failed to retrieve chapters due to database error")


@router.get("/{chapter_id}", response_model=Chapter)
async def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific textbook chapter by ID
    """
    logger.info(f"Retrieving chapter with ID: {chapter_id}")

    try:
        # Try to parse as UUID first, then as number
        try:
            uuid_obj = UUID(chapter_id)
            # Find chapter by UUID
            chapter = db.query(DBChapter).filter(DBChapter.id == uuid_obj, DBChapter.is_published == True).first()
        except ValueError:
            # If not a valid UUID, try to find by number
            try:
                chapter_number = int(chapter_id)
                chapter = db.query(DBChapter).filter(DBChapter.number == chapter_number, DBChapter.is_published == True).first()
            except ValueError:
                chapter = None

        if not chapter:
            raise ResourceNotFoundError(resource_type="Chapter", resource_id=chapter_id)

        # Convert DB chapter to Pydantic chapter
        chapter_response = Chapter(
            id=chapter.id,
            title=chapter.title,
            number=chapter.number,
            content=chapter.content,
            is_published=chapter.is_published,
            metadata=chapter.metadata_json,
            created_at=chapter.created_at,
            updated_at=chapter.updated_at or chapter.created_at
        )

        return chapter_response
    except ResourceNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapter {chapter_id}: {str(e)}", exc_info=True)
        raise DatabaseError(detail="Failed to retrieve chapter due to database error")


# Additional utility endpoint for content management (would require auth in real implementation)
@router.post("/index-content")
async def index_chapter_content(chapter_data: dict, db: Session = Depends(get_db)):
    """
    Index chapter content for the RAG system
    """
    try:
        from .chatbot_routes import rag_service  # Import here to avoid circular dependency

        chapter_id = chapter_data.get("chapter_id")
        content = chapter_data.get("content")

        if not chapter_id or not content:
            raise ValidationError("chapter_id and content are required")

        # Use the RAG service to index the content
        result = rag_service.index_content(chapter_id, content)
        logger.info(f"Successfully indexed content for chapter {chapter_id}")
        return result
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error indexing content for chapter {chapter_id}: {str(e)}", exc_info=True)
        raise DatabaseError(detail=f"Error indexing chapter content: {str(e)}")