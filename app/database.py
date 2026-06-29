from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = (
    f"sqlite:///{BASE_DIR}/approval.db"
)
import os
print("Database path:", os.path.abspath("approval.db"))

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

           
Base = declarative_base()
