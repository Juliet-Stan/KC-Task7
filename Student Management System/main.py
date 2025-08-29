#main.py

from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import logging
from datetime import datetime, timedelta
import time
import json
import os

from models import Student, StudentCreate, StudentUpdate, StudentResponse, User, Token
from database import get_session, create_db_and_tables
from auth import (
    authenticate_user, create_access_token, get_current_user,
    create_default_user, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY,
    get_password_hash, oauth2_scheme
)

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Student Management System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": process_time,
        "client_host": request.client.host if request.client else None
    }
    
    logging.info(f"Request: {log_data}")
    return response

# Initialize database and default user
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_default_user()

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    user = authenticate_user(username, password)
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

@app.post("/register")
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    # Check if user exists
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                users = json.load(f)
                if username in users:
                    raise HTTPException(status_code=400, detail="User already exists")
        else:
            users = {}
    except (json.JSONDecodeError, FileNotFoundError):
        users = {}
    
    # Add new user
    users[username] = {
        "username": username,
        "password": get_password_hash(password),
        "email": email
    }
    
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
    
    return {"message": "User created successfully"}

# Student CRUD endpoints
@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if email already exists
    existing_student = session.exec(select(Student).where(Student.email == student.email)).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Convert grades list to JSON string for storage
    grades_json = json.dumps(student.grades)
    
    db_student = Student(
        name=student.name,
        age=student.age,
        email=student.email,
        grades=grades_json
    )
    
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    
    # Convert back to list for response
    db_student.grades = student.grades
    return db_student

@app.get("/students/", response_model=List[StudentResponse])
async def read_students(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    students = session.exec(select(Student).offset(skip).limit(limit)).all()
    
    # Convert grades from JSON string to list
    for student in students:
        student.grades = json.loads(student.grades) if student.grades else []
    
    return students

@app.get("/students/{student_id}", response_model=StudentResponse)
async def read_student(
    student_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Convert grades from JSON string to list
    student.grades = json.loads(student.grades) if student.grades else []
    return student

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_student = session.get(Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_data_dict = student_data.model_dump(exclude_unset=True)
    
    for key, value in student_data_dict.items():
        if key == "grades" and value is not None:
            # Convert grades list to JSON string for storage
            setattr(db_student, key, json.dumps(value))
        else:
            setattr(db_student, key, value)
    
    db_student.updated_at = datetime.utcnow()
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    
    # Convert grades back to list for response
    db_student.grades = json.loads(db_student.grades) if db_student.grades else []
    return db_student

@app.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}

# Public endpoints
@app.get("/")
async def root():
    return {"message": "Student Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)