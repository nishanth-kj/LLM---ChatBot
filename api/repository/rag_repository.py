from repository.database.db import SessionLocal
from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from repository.database.db import Base
import numpy as np

class NewsEmbedding(Base):
    __tablename__ = "news_embeddings"
    
    news_id = Column(Integer, ForeignKey("news.news_id"), primary_key=True)
    embedding = Column(LargeBinary) # Stores numpy array as bytes

class RagRepository:
    def __init__(self):
        self.db = SessionLocal()

    def save_embedding(self, news_id, embedding_vec):
        # Convert numpy array to bytes
        blob = embedding_vec.tobytes()
        
        existing = self.db.query(NewsEmbedding).filter(NewsEmbedding.news_id == news_id).first()
        if existing:
            existing.embedding = blob
        else:
            new_emb = NewsEmbedding(news_id=news_id, embedding=blob)
            self.db.add(new_emb)
        self.db.commit()

    def get_all(self):
        return self.db.query(NewsEmbedding).all()

    def clear(self):
        self.db.query(NewsEmbedding).delete()
        self.db.commit()
