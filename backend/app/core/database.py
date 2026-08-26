# database.py — unchanged
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os 
from dotenv import load_dotenv

load_dotenv()

url =os.getenv("DATABASE_URL")
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()