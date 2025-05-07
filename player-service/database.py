from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = "postgresql://admin:auction_pass@192.168.56.225:5432/playerauction"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)    
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()