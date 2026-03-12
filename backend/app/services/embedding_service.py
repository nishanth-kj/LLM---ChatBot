from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for managing text embeddings"""
    
    def __init__(self):
        self.embeddings = None
        self._initialize()
    
    def _initialize(self):
        """Initialize embeddings model"""
        try:
            logger.info(f"Initializing embeddings model: {settings.embedding_model}...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model,
                model_kwargs={'device': settings.device}
            )
            logger.info("Embeddings model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing embeddings service: {e}")
            raise
    
    def get_embeddings(self):
        """Get the embeddings model instance"""
        return self.embeddings
