# Data Model: Textbook Platform with Chatbot

## Entities

### User
**Description**: Represents a platform user with authentication credentials, profile information, and learning history
**Fields**:
- id: UUID (primary key)
- email: string (unique, required)
- password_hash: string (required, hashed)
- first_name: string (optional)
- last_name: string (optional)
- created_at: timestamp (required)
- updated_at: timestamp (required)
- is_active: boolean (default: true)
- role: enum ['student', 'reader'] (default: 'reader')

**Validation**:
- Email must be valid email format
- Password must meet security requirements (min 8 chars, complexity)
- Email must be unique

**Relationships**:
- One-to-many with Question (user asks questions)
- One-to-many with LearningHistory (user progress)

### Chapter
**Description**: Represents one of the 6 textbook chapters with content, metadata, and citation information
**Fields**:
- id: UUID (primary key)
- title: string (required)
- number: integer (required, 1-6)
- content: text (required, markdown format)
- metadata: JSON (optional, additional chapter info)
- created_at: timestamp (required)
- updated_at: timestamp (required)
- is_published: boolean (default: true)

**Validation**:
- Number must be between 1-6
- Title and content required
- Unique constraint on number per textbook

**Relationships**:
- One-to-many with ContentChunk (chapter contains chunks for AI)
- One-to-many with Citation (chapter has citations)

### Question
**Description**: Represents a user's query submitted to the chatbot with timestamp and context
**Fields**:
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- question_text: text (required)
- chapter_context_id: UUID (foreign key to Chapter, optional)
- created_at: timestamp (required)
- updated_at: timestamp (required)
- status: enum ['pending', 'processed', 'error'] (default: 'pending')

**Validation**:
- Question text required
- Valid user_id if authenticated
- Valid chapter_context_id if provided

**Relationships**:
- Many-to-one with User (user asks question)
- Many-to-one with Chapter (optional context)
- One-to-one with Answer (question has answer)

### Answer
**Description**: Represents the chatbot's response with citations to source material and confidence level
**Fields**:
- id: UUID (primary key)
- question_id: UUID (foreign key to Question, unique)
- answer_text: text (required)
- citations: JSON array (required, source references)
- confidence_score: float (0.0-1.0, required)
- created_at: timestamp (required)
- updated_at: timestamp (required)

**Validation**:
- Answer text required
- Question_id must be unique
- Confidence score between 0.0-1.0
- Citations must be valid format

**Relationships**:
- Many-to-one with Question (answer to question)

### ContentChunk
**Description**: Represents a chunk of textbook content for vector search in the RAG pipeline
**Fields**:
- id: UUID (primary key)
- chapter_id: UUID (foreign key to Chapter)
- content: text (required, chunked content)
- embedding_vector: vector (required, for similarity search)
- chunk_metadata: JSON (optional, additional metadata)
- created_at: timestamp (required)

**Validation**:
- Content required
- Valid chapter_id
- Embedding vector must be properly formatted

**Relationships**:
- Many-to-one with Chapter (chunk belongs to chapter)

### LearningHistory
**Description**: Tracks user interaction with textbook content for progress tracking
**Fields**:
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- chapter_id: UUID (foreign key to Chapter)
- last_accessed: timestamp (required)
- progress_percentage: float (0.0-100.0, optional)
- time_spent: integer (seconds, optional)
- created_at: timestamp (required)
- updated_at: timestamp (required)

**Validation**:
- Valid user_id and chapter_id
- Progress percentage between 0.0-100.0
- Time spent non-negative

**Relationships**:
- Many-to-one with User (user's history)
- Many-to-one with Chapter (chapter in history)

## State Transitions

### Question States
- **pending**: Question received, waiting for processing
- **processed**: Question processed, answer generated
- **error**: Error occurred during processing

### User Roles
- **reader**: Can view textbook content
- **student**: Can view content and use chatbot features