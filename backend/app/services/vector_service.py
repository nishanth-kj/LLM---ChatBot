from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.embedding_service import EmbeddingService
from langchain_community.vectorstores import FAISS
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Service for managing vector store operations"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.embeddings = self.embedding_service.get_embeddings()
        self.vector_store = None
        self._initialize()
    
    def _initialize(self):
        """Initialize embeddings and vector store"""
        try:
            logger.info("Initializing embeddings...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model,
                model_kwargs={'device': settings.device}
            )
            
            # Check if vector store exists
            vectorstore_path = Path(settings.vectorstore_path)
            if vectorstore_path.exists() and (vectorstore_path / "index.faiss").exists():
                logger.info("Loading existing vector store...")
                self.vector_store = FAISS.load_local(
                    str(vectorstore_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                logger.info("Creating new vector store from documents...")
                self._create_vector_store()
            
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def _create_vector_store(self):
        """Create vector store from PDF documents"""
        data_path = Path(settings.data_path)
        
        if not data_path.exists():
            logger.warning(f"Data path {data_path} does not exist. Creating empty vector store.")
            # Create a minimal vector store with a placeholder document
            from langchain.schema import Document
            docs = [Document(page_content="Healthcare information placeholder", metadata={})]
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
            return
        
        # Load PDF documents
        logger.info(f"Loading documents from {data_path}...")
        loader = DirectoryLoader(
            str(data_path),
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        
        if not documents:
            logger.warning("No PDF documents found. Creating empty vector store.")
            from langchain.schema import Document
            docs = [Document(page_content="Healthcare information placeholder", metadata={})]
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
            return
        
        # Split documents into chunks
        logger.info(f"Splitting {len(documents)} documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        text_chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(text_chunks)} text chunks")
        
        # Create vector store
        logger.info("Creating FAISS vector store...")
        self.vector_store = FAISS.from_documents(text_chunks, self.embeddings)
        
        # Save vector store
        vectorstore_path = Path(settings.vectorstore_path)
        vectorstore_path.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(str(vectorstore_path))
        logger.info(f"Vector store saved to {vectorstore_path}")
    
    def get_retriever(self, k: int = None):
        """Get retriever for similarity search"""
        if k is None:
            k = settings.retrieval_k
        return self.vector_store.as_retriever(search_kwargs={"k": k})
