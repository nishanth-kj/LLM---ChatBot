from pathlib import Path
from langchain_community.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from core.config import settings
from services.vector_service import VectorStoreService
from utils.logger import logger
import os

from repository.setting_repository import SettingRepository

class LLMService:
    """Service for managing LLM operations and Playground"""
    
    def __init__(self):
        self.llm = None
        self.vector_store_service = None
        self.chain = None
        self.memory = None
        self.setting_repo = SettingRepository()
        
        # Determine models directory
        self.models_dir = Path(settings.model_path).parent
        if not self.models_dir.exists():
            self.models_dir.mkdir(parents=True, exist_ok=True)
            
        # Restore active model from database repository if registered
        saved_model = self.setting_repo.get("current_model")
        if saved_model:
            self.current_model = saved_model
            settings.model_path = str(self.models_dir / saved_model)
        else:
            self.current_model = Path(settings.model_path).name
            
        self._initialize()
    
    def get_available_models(self):
        """List all available models in the models directory"""
        try:
            if not self.models_dir.exists():
                return []
            return [f.name for f in self.models_dir.glob("*.gguf")] + [f.name for f in self.models_dir.glob("*.bin")]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def switch_model(self, model_filename: str):
        """Switch the current LLM to a new model"""
        model_path = self.models_dir / model_filename
        if not model_path.exists():
            raise FileNotFoundError(f"Model {model_filename} not found in {self.models_dir}")
        
        logger.info(f"Switching to model: {model_filename}")
        self.current_model = model_filename
        settings.model_path = str(model_path)
        
        # Persist model selection in Postgres database settings table using repository layout
        self.setting_repo.set("current_model", model_filename)
        
        # Re-initialize with new model
        self._initialize_llm(model_path)
        self._initialize_chain()
        return True

    def _initialize(self):
        """Initialize LLM, vector store, and conversation chain"""
        try:
            logger.info("Initializing vector store service...")
            self.vector_store_service = VectorStoreService()
            
            # Initialize memory
            logger.info("Initializing conversation memory...")
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            model_path = Path(settings.model_path)
            if not model_path.exists():
                logger.warning(f"Default model file not found at {model_path}. Will need to load a model manually.")
            else:
                self._initialize_llm(model_path)
                self._initialize_chain()
                
            logger.info("LLM service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LLM service: {e}")
            raise

    def _initialize_llm(self, model_path: Path):
        logger.info(f"Loading LLM model from {model_path}...")
        self.llm = CTransformers(
            model=str(model_path),
            model_type=settings.model_type,
            config={
                'max_new_tokens': settings.max_new_tokens,
                # 'temperature': settings.temperature  # add back if settings has it
            }
        )

    def _initialize_chain(self):
        logger.info("Creating conversation chain...")
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            chain_type='stuff',
            retriever=self.vector_store_service.get_retriever(),
            memory=self.memory
        )
    
    def get_response(self, question: str) -> str:
        """Get response from the LLM for a given question"""
        try:
            if not self.is_initialized:
                return "Error: No model loaded. Please load a model first."
                
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
        if self.memory:
            self.memory.clear()
            logger.info("Conversation memory reset")
    
    @property
    def is_initialized(self) -> bool:
        """Check if the service is properly initialized"""
        return self.llm is not None and self.chain is not None
