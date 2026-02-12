# Quickstart Guide: Textbook Platform with Chatbot

## Overview
This guide will help you set up and run the textbook platform with chatbot functionality. The system consists of three main components: frontend (Docusaurus), backend (FastAPI), and AI pipeline (RAG processing).

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon account)
- Qdrant vector database
- Claude API access

## Setup Instructions

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart psycopg2-binary sqlalchemy asyncpg sentence-transformers

# Set environment variables
cp .env.example .env
# Edit .env with your database and API credentials

# Run the backend server
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env with backend API URL

# Build and serve the frontend
npm run build
npm run serve  # For production
# OR
npm start      # For development
```

### 4. AI Pipeline Setup
```bash
# Navigate to AI pipeline directory
cd ai-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install sentence-transformers qdrant-client transformers torch

# Set environment variables
cp .env.example .env
# Edit .env with Qdrant and Claude API credentials

# Run the AI pipeline to process textbook content
python -m src.chunking.process_content
```

### 5. Database Setup
```bash
# With backend virtual environment activated
cd backend

# Run database migrations
python -m src.database.migrate
```

### 6. Initialize Textbook Content
```bash
# Generate or import the 6 textbook chapters
# Place markdown files in frontend/docs/chapters/

# Process chapters for AI pipeline
cd ai-pipeline
python -m src.chunking.process_content
```

## Running the Application

### Development Mode
1. Start Qdrant (vector database):
```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

2. Start backend:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

3. Start frontend:
```bash
cd frontend
npm start
```

4. Process textbook content:
```bash
cd ai-pipeline
python -m src.chunking.process_content
```

### Production Mode
1. Deploy backend to server with gunicorn:
```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. Build and serve frontend:
```bash
cd frontend
npm run build
npx serve -s build
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user

### Chapters
- `GET /api/v1/chapters` - Get all chapters
- `GET /api/v1/chapters/{id}` - Get specific chapter

### Chatbot
- `POST /api/v1/chatbot/ask` - Ask a question about textbook content
- `GET /api/v1/chatbot/history` - Get user's question history

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
QDRANT_HOST=localhost
QDRANT_PORT=6333
CLAUDE_API_KEY=your-claude-api-key
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

## Troubleshooting

1. **Qdrant Connection Issues**: Ensure Qdrant is running and accessible at the configured host/port
2. **Database Connection**: Verify DATABASE_URL is correct and database is running
3. **Claude API**: Check that CLAUDE_API_KEY is valid and has appropriate permissions
4. **CORS Issues**: Ensure frontend origin is allowed in backend CORS settings

## Next Steps

1. Customize the Docusaurus theme to match your branding
2. Add more textbook chapters as needed
3. Fine-tune the AI pipeline for better responses
4. Implement additional user features like progress tracking