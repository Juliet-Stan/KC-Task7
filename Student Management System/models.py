#models.py

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr
import json

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int
    email: str = Field(unique=True, index=True)
    grades: str = Field(default="")  # Store as JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StudentCreate(SQLModel):
    name: str
    age: int
    email: str
    grades: List[str] = []  # Accept list of grades

class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    grades: Optional[List[str]] = None

class StudentResponse(SQLModel):
    id: int
    name: str
    age: int
    email: str
    grades: List[str]
    created_at: datetime
    updated_at: datetime

class User(SQLModel):
    username: str
    password: str
    email: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None