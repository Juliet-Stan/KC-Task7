#dependencies.py

from fastapi import HTTPException, status
from sqlmodel import Session, select
from database import get_session
from auth import get_current_user
from models import User, JobApplication

def get_db_session():
    return next(get_session())

def verify_application_ownership(application_id: int, current_user: User, session: Session):
    application = session.get(JobApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this application")
    return application