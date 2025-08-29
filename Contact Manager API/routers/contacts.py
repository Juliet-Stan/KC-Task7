#contacts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from models import Contact, ContactCreate, ContactUpdate, ContactResponse, User
from database import get_session
from auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])

def verify_contact_ownership(contact_id: int, current_user: User, session: Session):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this contact")
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if contact with same email already exists for this user
    if contact.email:
        existing_contact = session.exec(
            select(Contact).where(
                Contact.email == contact.email,
                Contact.user_id == current_user.id
            )
        ).first()
        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact with this email already exists"
            )
    
    db_contact = Contact(
        **contact.dict(),
        user_id=current_user.id
    )
    
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    
    return db_contact

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Build query based on search parameter
    query = select(Contact).where(Contact.user_id == current_user.id)
    
    if search:
        query = query.where(
            (Contact.name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%")) |
            (Contact.phone.ilike(f"%{search}%"))
        )
    
    query = query.offset(skip).limit(limit).order_by(Contact.name)
    
    contacts = session.exec(query).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    contact = verify_contact_ownership(contact_id, current_user, session)
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    contact = verify_contact_ownership(contact_id, current_user, session)
    
    # Check if email is being updated and if it conflicts with existing contact
    if contact_data.email and contact_data.email != contact.email:
        existing_contact = session.exec(
            select(Contact).where(
                Contact.email == contact_data.email,
                Contact.user_id == current_user.id,
                Contact.id != contact_id
            )
        ).first()
        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact with this email already exists"
            )
    
    # Update contact data
    update_data = contact_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)
    
    contact.updated_at = datetime.utcnow()
    session.add(contact)
    session.commit()
    session.refresh(contact)
    
    return contact

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    contact = verify_contact_ownership(contact_id, current_user, session)
    session.delete(contact)
    session.commit()
    
    return {"message": "Contact deleted successfully"}

@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(
    q: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Contact).where(
        Contact.user_id == current_user.id
    ).where(
        (Contact.name.ilike(f"%{q}%")) |
        (Contact.email.ilike(f"%{q}%")) |
        (Contact.phone.ilike(f"%{q}%")) |
        (Contact.address.ilike(f"%{q}%"))
    ).order_by(Contact.name)
    
    contacts = session.exec(query).all()
    return contacts