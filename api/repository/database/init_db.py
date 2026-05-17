from repository.database.db import engine, Base
from repository.setting_repository import Setting
from repository.chat_repository import ChatHistory

def init_db():
    Base.metadata.create_all(bind=engine)