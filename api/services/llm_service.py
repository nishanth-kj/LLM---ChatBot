from pathlib import Path
from langchain_community.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from app.core.config import settings
from app.services.vector_service import VectorStoreService
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for managing LLM operations"""
    
    def __init__(self):
        self.llm = None
        self.vector_store_service = None
        self.chain = None
        self.memory = None
        self._initialize()
    
    def _initialize(self):
        """Initialize LLM, vector store, and conversation chain"""
        try:
            # Initialize vector store
            logger.info("Initializing vector store service...")
            self.vector_store_service = VectorStoreService()
            
            # Initialize LLM
            model_path = Path(settings.model_path)
            if not model_path.exists():
                logger.error(f"Model file not found at {model_path}")
                raise FileNotFoundError(
                    f"Model file not found at {model_path}. "
                    f"Please download the model and place it in the models directory."
                )
            
            logger.info(f"Loading LLM model from {model_path}...")
            self.llm = CTransformers(
                model=str(model_path),
                model_type=settings.model_type,
                config={
                    'max_new_tokens': settings.max_new_tokens,
                    'temperature': settings.temperature
                }
            )
            
            # Initialize memory
            logger.info("Initializing conversation memory...")
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Initialize conversation chain
            logger.info("Creating conversation chain...")
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                chain_type='stuff',
                retriever=self.vector_store_service.get_retriever(),
                memory=self.memory
            )
            
            logger.info("LLM service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LLM service: {e}")
            raise
    
    def get_response(self, question: str) -> str:
        """Get response from the LLM for a given question"""
        try:
            logger.info(f"Processing question: {question[:50]}...")
            result = self.chain({"question": question})
            answer = result.get("answer", "I'm sorry, I couldn't generate a response.")
            logger.info(f"Generated answer: {answer[:50]}...")
            return answer
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def reset_memory(self):
        """Reset conversation memory"""
        self.memory.clear()
        logger.info("Conversation memory reset")
    
    @property
    def is_initialized(self) -> bool:
        """Check if the service is properly initialized"""
        return self.llm is not None and self.chain is not None
