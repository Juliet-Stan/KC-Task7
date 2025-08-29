routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta

from models import User
from schemas import UserCreate, UserResponse, Token
from database import get_session
from auth import (
    get_user_by_username, get_password_hash,
    create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if username already exists
    if get_user_by_username(session, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at
    )

@router.post("/login", response_model=Token)
async def login_user(
    username: str,
    password: str,
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}