from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    app_name: str = "ChatBot Desktop API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS Configuration
    cors_origins: list[str] = ["*"]
    
    # Model Configuration
    # Relative to project root if running from root, or use absolute path
    model_path: str = "../models/mistral-7b-instruct.Q4_K_M.gguf"
    model_type: str = "mistral"
    max_new_tokens: int = 512
    temperature: float = 0.7
    
    # Embedding Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = "cpu"
    
    # Document Configuration
    data_path: str = "data/documents"
    vectorstore_path: str = "data/vectorstore"
    chunk_size: int = 1000
    chunk_overlap: int = 100
    
    # Retrieval Configuration
    retrieval_k: int = 4
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
