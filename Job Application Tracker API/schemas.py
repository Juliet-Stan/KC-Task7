from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel

class JobApplicationCreate(BaseModel):
    company: str
    position: str
    status: str
    date_applied: datetime
    notes: Optional[str] = None

class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    date_applied: Optional[datetime] = None
    notes: Optional[str] = None

class JobApplicationRead(BaseModel):
    id: int
    company: str
    position: str
    status: str
    date_applied: datetime
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(SQLModel):
    username: str
    password: str