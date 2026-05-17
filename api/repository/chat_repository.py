from sqlalchemy import Column, Integer, String, Text, BigInteger
from repository.database.db import Base, SessionLocal
from utils.time_utils import TimeUtils

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    system_prompt = Column(Text)
    input_text = Column(Text)
    response_text = Column(Text)
    created_at = Column(BigInteger, default=TimeUtils.now_epoch)

class ChatRepository:
    def __init__(self):
        self.db = SessionLocal()

    def save(self, model: str, system_prompt: str, input_text: str, response_text: str):
        chat = ChatHistory(
            model=model,
            system_prompt=system_prompt,
            input_text=input_text,
            response_text=response_text,
            created_at=TimeUtils.now_epoch()
        )
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat
