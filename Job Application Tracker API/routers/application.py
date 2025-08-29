#applications.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from models import JobApplication, User
from schemas import JobApplicationCreate, JobApplicationRead, JobApplicationUpdate
from database import get_session
from auth import get_current_user
from dependencies import verify_application_ownership

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=JobApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_job_application(
    application: JobApplicationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Validate status
    valid_statuses = ["pending", "interview", "rejected", "offered", "accepted"]
    if application.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    db_application = JobApplication(
        **application.dict(),
        user_id=current_user.id
    )
    
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application

@router.get("/", response_model=List[JobApplicationRead])
async def read_job_applications(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(JobApplication).where(
        JobApplication.user_id == current_user.id
    ).offset(skip).limit(limit)
    
    applications = session.exec(statement).all()
    return applications

@router.get("/{application_id}", response_model=JobApplicationRead)
async def read_job_application(
    application_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    application = verify_application_ownership(application_id, current_user, session)
    return application

@router.get("/search/", response_model=List[JobApplicationRead])
async def search_job_applications(
    status: Optional[str] = Query(None, description="Filter by application status"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Build query based on filters
    query = select(JobApplication).where(JobApplication.user_id == current_user.id)
    
    if status:
        valid_statuses = ["pending", "interview", "rejected", "offered", "accepted"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(valid_statuses)}"
            )
        query = query.where(JobApplication.status == status)
    
    if company:
        query = query.where(JobApplication.company.ilike(f"%{company}%"))
    
    applications = session.exec(query).all()
    return applications

@router.put("/{application_id}", response_model=JobApplicationRead)
async def update_job_application(
    application_id: int,
    application_data: JobApplicationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    application = verify_application_ownership(application_id, current_user, session)
    
    # Validate status if provided
    if application_data.status:
        valid_statuses = ["pending", "interview", "rejected", "offered", "accepted"]
        if application_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(valid_statuses)}"
            )
    
    # Update application data
    update_data = application_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)
    
    application.updated_at = datetime.utcnow()
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@router.delete("/{application_id}")
async def delete_job_application(
    application_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    application = verify_application_ownership(application_id, current_user, session)
    session.delete(application)
    session.commit()
    return {"message": "Application deleted successfully"}