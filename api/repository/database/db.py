from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///chatbot.db"
)

# Use postgres or fallback to sqlite if needed
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # Postgres configuration
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()