from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/", response_model=List[ContactResponse],
    description='No more than 10 requests per minute',
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def read_contacts(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :param : Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(
        skip, limit, current_user, db
    )
    return contacts


@router.get(
    "/{contact_id}", response_model=ContactResponse,
    description='No more than 10 requests per minute',
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def read_contact(
        contact_id: int, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_contact function is a GET endpoint that returns the contact with the given ID.
    It requires authentication and authorization, so it uses auth_service to get the current user.
    If no contact exists with this ID, it raises an HTTPException.

    :param contact_id: int: Specify the id of the contact
    :param db: Session: Get a database session
    :param current_user: User: Get the user who is making the request
    :param : Get the contact id
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(
        contact_id, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    description='No more than 10 requests per minute',
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def create_contact(
        body: ContactCreate, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactCreate: Pass the body of the request to
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user id of the current
    :param : Get the contact id from the path
    :return: The created contact
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(
        body, current_user, db
    )


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
        body: ContactUpdate, contact_id: int, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.

    :param body: ContactUpdate: Get the data from the request body
    :param contact_id: int: Specify the contact to be deleted
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the
    :param : Get the contact id

    :return: A contact object

    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(
        contact_id, body, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
        contact_id: int, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to remove
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :param : Get the contact id

    :return: A contact object

    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(
        contact_id, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts_api(
    first_name: str = "", last_name: str = "", email: str = "",
        db: Session = Depends(get_db),
):
    """
    The search_contacts_api function searches for contacts in the database.
        It takes three optional parameters: first_name, last_name, and email.
        If no parameters are provided, it returns all contacts in the database.

    :param first_name: str: Search for contacts by first name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Search for a contact by email
    :param db: Session: Pass the database session to the repository layer
    :param : Get the data from the database

    :return: A list of contacts

    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(
        first_name=first_name, last_name=last_name, email=email, db=db
    )
    return contacts


@router.get("/upcoming-birthdays/", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    """
    The get_upcoming_birthdays function returns a list of contacts with upcoming birthdays.

    :param db: Session: Pass the database session into the function

    :return: A list of contacts

    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_upcoming_birthdays(db)
    return contacts
