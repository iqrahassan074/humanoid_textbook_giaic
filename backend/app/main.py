from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from dotenv import load_dotenv

load_dotenv()

from src.api.chatbot_routes import router as chatbot_router
from src.api.chapter_routes import router as chapter_router
from src.api.auth_routes import router as auth_router

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application
    """
    # Startup events
    logger.info("Starting up the textbook chatbot API")

    # Initialize services if needed
    # For example: initialize database connections, caches, etc.

    yield  # Application runs here

    # Shutdown events
    logger.info("Shutting down the textbook chatbot API")


# Create FastAPI app instance
app = FastAPI(
    title="Textbook Chatbot API",
    description="API for textbook platform with AI-powered Q&A functionality",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chatbot_router)
app.include_router(chapter_router)
app.include_router(auth_router)

# Add a simple health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Textbook Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "textbook-chatbot-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)