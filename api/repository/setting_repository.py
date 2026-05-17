from repository.database.db import SessionLocal
from sqlalchemy import Column, String, Text
from repository.database.db import Base

class Setting(Base):
    __tablename__ = "settings"
    
    key = Column(String, primary_key=True)
    value = Column(Text)

class SettingRepository:
    def __init__(self):
        self.db = SessionLocal()

    def set(self, key, value):
        setting = self.db.query(Setting).filter(Setting.key == key).first()
        if setting:
            setting.value = value
        else:
            setting = Setting(key=key, value=value)
            self.db.add(setting)
        self.db.commit()

    def get(self, key, default=None):
        setting = self.db.query(Setting).filter(Setting.key == key).first()
        return setting.value if setting else default

    def get_all(self):
        return self.db.query(Setting).all()
