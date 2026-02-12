# Physical AI Textbook Platform

A comprehensive textbook platform with AI-powered Q&A functionality for learning about Physical AI and Humanoid Robotics. This project implements a full-stack solution with textbook content, user authentication, and an intelligent chatbot that answers questions with proper citations.

## 🌟 Features

### Textbook Platform
- 6 comprehensive chapters on Physical AI topics
- Docusaurus-based frontend for excellent reading experience
- Mobile-responsive design
- Chapter navigation and search capabilities

### AI Assistant
- Q&A system using Retrieval-Augmented Generation (RAG)
- Answers grounded in textbook content (zero hallucination)
- Proper citations for all information sources
- Confidence scoring for answer reliability

### User Management
- User registration and authentication
- JWT-based security
- Personalized learning experience

### Technical Architecture
- Modular design with separate frontend, backend, and AI pipeline
- Free-tier friendly infrastructure (PostgreSQL via Neon, Qdrant)
- Hackathon-ready with quick setup and deployment

## 🏗️ Architecture

### Frontend
- **Framework**: Docusaurus
- **Language**: React, JavaScript/TypeScript
- **Features**: Textbook reader, AI chatbot widget, authentication UI

### Backend
- **Framework**: FastAPI
- **Language**: Python
- **API**: RESTful endpoints for auth, chapters, and chatbot

### AI Pipeline
- **Embeddings**: sentence-transformers
- **Vector DB**: Qdrant
- **AI Model**: Claude for answer generation
- **RAG**: Retrieval-Augmented Generation pipeline

## 📁 Project Structure

```
hackathonn/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── api/           # API routes
│   └── main.py            # Application entry point
├── frontend/               # Docusaurus frontend
│   ├── docs/              # Textbook chapters
│   ├── src/               # React components
│   │   ├── components/    # UI components
│   │   ├── contexts/      # React contexts
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   ├── docusaurus.config.js
│   └── package.json
├── ai-pipeline/            # AI processing pipeline
│   ├── src/
│   │   ├── chunking/      # Content chunking
│   │   ├── embedding/     # Embedding generation
│   │   └── rag/          # RAG implementation
├── specs/002-textbook-chatbot/  # Project specifications
│   ├── spec.md           # Feature specification
│   ├── plan.md           # Implementation plan
│   ├── tasks.md          # Task breakdown
│   └── contracts/        # API contracts
└── history/prompts/      # Prompt history records
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for Qdrant)
- Claude API key

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart psycopg2-binary sqlalchemy asyncpg sentence-transformers qdrant-client anthropic

# Set environment variables
cp .env.example .env
# Edit .env with your Claude API key and database settings

# Run the backend server
uvicorn main:app --reload --port 8000
```

### AI Pipeline Setup
```bash
# Navigate to AI pipeline directory
cd ai-pipeline

# Activate the same virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if not already installed)
pip install sentence-transformers qdrant-client anthropic

# Process textbook content (after frontend chapters are created)
python -c "
from src.chunking.chunker import TextChunker
from src.embedding.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.claude_processor import ClaudeProcessor

# Initialize components
chunker = TextChunker()
embedder = Embedder()
vector_store = VectorStore()
# claude_processor = ClaudeProcessor()  # If API key is available
"
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set backend API URL in .env
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

### Vector Database (Qdrant)
```bash
# Run Qdrant in Docker
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
QDRANT_HOST=localhost
QDRANT_PORT=6333
CLAUDE_API_KEY=your-claude-api-key
```

#### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## 📚 Textbook Content

The platform includes 6 comprehensive chapters:

1. **Introduction to Physical AI** - Fundamental concepts and historical context
2. **Robotics and AI Integration** - How robotics and AI converge
3. **Sensorimotor Learning** - Learning through physical interaction
4. **Human-Robot Interaction** - Principles of human-robot collaboration
5. **Embodied Intelligence** - Intelligence emerging from physical form
6. **Future of Physical AI** - Emerging trends and applications

## 🤖 AI Assistant Features

The AI assistant provides:
- Answers based only on textbook content (no hallucinations)
- Proper citations to source chapters and sections
- Confidence scoring for answer reliability
- Context-aware responses
- Natural language interaction

### How the RAG Pipeline Works
1. User sends query
2. Backend embeds query using sentence-transformers
3. Qdrant performs similarity search (top 5 chunks)
4. Retrieved chunks are sent to Claude
5. Claude generates answer with citations
6. Response is returned to user

## 🛡️ Security & Compliance

- JWT-based authentication
- Rate limiting (10 req/min/IP)
- CORS restricted to frontend domain
- Secure password hashing
- Input validation and sanitization

## 🚀 Deployment

### Frontend
- Build: `npm run build`
- Deploy to: GitHub Pages, Netlify, Vercel, or any static hosting

### Backend
- Deploy to: Railway, Heroku, AWS, or any Python-compatible platform
- Ensure environment variables are configured
- Database and Qdrant must be accessible

## 🧪 Testing

### Backend Tests
```bash
# Run backend tests
pytest tests/
```

### Frontend Tests
```bash
# Run frontend tests
npm test
```

## 📈 Performance Goals

- Page load < 2 seconds
- API p95 < 2 seconds
- 95% of chatbot responses include proper citations
- 90% of users can navigate on mobile without issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository.

---

Built with ❤️ for the Physical AI community. This project demonstrates how modern AI techniques can enhance educational experiences while maintaining accuracy and explainability.