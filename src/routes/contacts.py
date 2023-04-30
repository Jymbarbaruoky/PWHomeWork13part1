from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 1 contact per minute',
             dependencies=[Depends(RateLimiter(seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         _current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, db)


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                        _current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       _current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         _current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/query/", response_model=List[ContactResponse])
async def querys_contacts(firstname: str = '', lastname: str = '', email: str = '', db: Session = Depends(get_db),
                          _current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.querys_contacts(firstname, lastname, email, db)
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def birthdays(db: Session = Depends(get_db), _current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.birthdays(db)
    return contacts
