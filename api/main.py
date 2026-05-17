from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from models.schemas import HealthResponse
from services.llm_service import LLMService
from routes import chat
from utils.logger import logger
from utils.api_response import ApiResponse

# Global LLM service instance
llm_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global llm_service
    
    # Startup
    logger.info("Starting up application...")
    try:
        llm_service = LLMService()
        # Inject llm_service into app state so routers can access it
        app.state.llm_service = llm_service
        logger.info("LLM service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize LLM service: {e}")
        logger.warning("Application will start but LLM functionality may be limited")
        app.state.llm_service = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Healthcare ChatBot API powered by LLMs (Playground Mode)",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/health")
async def health_check():
    """Health check endpoint using ApiResponse util"""
    is_loaded = llm_service is not None and llm_service.is_initialized
    return ApiResponse.success({
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "model_loaded": is_loaded,
        "current_model": llm_service.current_model if is_loaded else None
    })

@app.get("/")
async def root():
    """Root endpoint"""
    return ApiResponse.success({
        "message": "LLM Playground API",
        "version": settings.app_version,
        "docs": "/docs"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
