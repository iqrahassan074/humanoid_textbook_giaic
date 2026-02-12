from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from passlib.context import CryptContext
import uuid
from datetime import datetime
import os

# Database configuration - using SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./textbook_app.db")

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    is_active = Column(Boolean, default=True)
    role = Column(String, default='reader')  # 'reader' or 'student'

    # Relationships
    questions = relationship("Question", back_populates="user")
    learning_histories = relationship("LearningHistory", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    number = Column(Integer, nullable=False)  # 1-6 for textbook chapters
    content = Column(Text, nullable=False)
    metadata_json = Column(Text)  # JSON metadata as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    is_published = Column(Boolean, default=True)

    # Relationships
    content_chunks = relationship("ContentChunk", back_populates="chapter")
    questions = relationship("Question", back_populates="chapter_context")
    learning_histories = relationship("LearningHistory", back_populates="chapter")


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    chapter_context_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"))  # Optional
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    status = Column(String, default='pending')  # 'pending', 'processed', 'error'

    # Relationships
    user = relationship("User", back_populates="questions")
    chapter_context = relationship("Chapter", back_populates="questions")
    answer = relationship("Answer", uselist=False, back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), unique=True, nullable=False)
    answer_text = Column(Text, nullable=False)
    citations = Column(Text)  # JSON citations as text
    confidence_score = Column(Integer)  # 0-100 scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    question = relationship("Question", back_populates="answer")


class ContentChunk(Base):
    __tablename__ = "content_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding_vector = Column(Text)  # Vector as text representation
    chunk_metadata = Column(Text)  # JSON metadata as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chapter = relationship("Chapter", back_populates="content_chunks")


class LearningHistory(Base):
    __tablename__ = "learning_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    progress_percentage = Column(Integer)  # 0-100
    time_spent = Column(Integer)  # seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_histories")
    chapter = relationship("Chapter", back_populates="learning_histories")


# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)