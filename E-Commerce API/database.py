#database.py

from sqlmodel import SQLModel, create_engine, Session
import os

# SQLite database URL
DATABASE_URL = "sqlite:///./ecommerce.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session