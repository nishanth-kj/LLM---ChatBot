from repository.database.db import engine, Base
from repository.meme_repository import Meme
from repository.news_repository import News
from repository.setting_repository import Setting
from repository.rag_repository import NewsEmbedding
from repository.chat_repository import ChatHistory

def init_db():
    Base.metadata.create_all(bind=engine)