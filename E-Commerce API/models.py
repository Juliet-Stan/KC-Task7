#models.py

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr
import json

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    stock: int
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(SQLModel):
    name: str
    price: float
    stock: int
    description: Optional[str] = None

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    description: Optional[str] = None

class ProductResponse(SQLModel):
    id: int
    name: str
    price: float
    stock: int
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False

class UserResponse(SQLModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None

class CartItem(SQLModel):
    product_id: int
    quantity: int
    name: str
    price: float

class Cart(SQLModel):
    items: List[CartItem] = []
    total: float = 0.0

class OrderItem(SQLModel):
    product_id: int
    quantity: int
    price: float
    name: str

class Order(SQLModel):
    id: Optional[int] = None
    user_id: int
    items: List[OrderItem]
    total: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)