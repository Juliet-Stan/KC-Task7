#notes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import json
from datetime import datetime

from models import Note, NoteCreate, NoteUpdate, NoteResponse, User
from database import get_session
from auth import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])

def save_notes_to_json(notes: List[Note]):
    """Save all notes to JSON file for backup"""
    notes_data = []
    for note in notes:
        notes_data.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "user_id": note.user_id
        })
    
    with open("notes.json", "w") as f:
        json.dump(notes_data, f, indent=2, default=str)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=current_user.id
    )
    
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    
    # Update backup file
    all_notes = session.exec(select(Note)).all()
    save_notes_to_json(all_notes)
    
    return db_note

@router.get("/", response_model=List[NoteResponse])
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Note).where(
        Note.user_id == current_user.id
    ).offset(skip).limit(limit)
    
    notes = session.exec(statement).all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")
    
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
    
    # Update note data
    update_data = note_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    
    note.updated_at = datetime.utcnow()
    session.add(note)
    session.commit()
    session.refresh(note)
    
    # Update backup file
    all_notes = session.exec(select(Note)).all()
    save_notes_to_json(all_notes)
    
    return note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    
    session.delete(note)
    session.commit()
    
    # Update backup file
    all_notes = session.exec(select(Note)).all()
    save_notes_to_json(all_notes)
    
    return {"message": "Note deleted successfully"}