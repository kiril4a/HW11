from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from repository import contacts as contact_repository
from schemas import ContactCreate, ContactUpdate, ContactInDB

router = APIRouter()

@router.post("/", response_model=ContactInDB)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contact_repository.create_contact(db, contact)

@router.get("/", response_model=List[ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return contact_repository.get_contacts(db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = contact_repository.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactInDB)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = contact_repository.update_contact(db, contact_id, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}", response_model=ContactInDB)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = contact_repository.delete_contact(db, contact_id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact

@router.get("/search/", response_model=List[ContactInDB])
def search_contacts(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return contact_repository.search_contacts(db, query)

@router.get("/upcoming_birthdays/", response_model=List[ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return contact_repository.get_upcoming_birthdays(db)
