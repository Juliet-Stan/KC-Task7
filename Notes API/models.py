#models.py

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

class NoteCreate(SQLModel):
    title: str
    content: str

class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(SQLModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: int
    username: str
    email: str
    created_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str