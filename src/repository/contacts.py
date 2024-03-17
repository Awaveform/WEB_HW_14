from datetime import datetime, timedelta
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate


async def get_contacts(
        skip: int, limit: int, user: User, db: Session
) -> list[Type[Contact]]:
    """
    The get_contacts function returns a list of contacts for the user.
    
    :param skip: int: Skip the first n contacts in the list
    :param limit: int: Limit the number of results returned
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database

    :return: A list of contact objects

    :doc-author: Trelent
    """
    return db.query(Contact).filter(
        Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(
        contact_id: int, user: User, db: Session
) -> Type[Contact] | None:
    """
    The get_contact function takes in a contact_id, user, and db.
    It returns the Contact object with the given id if it exists for that user.
    Otherwise, it returns None.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function

    :return: A contact object or none

    :doc-author: Trelent
    """
    return db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == user.id).first()


async def create_contact(body: ContactCreate, user: User, db: Session) -> Contact:

    """
    The create_contact function creates a new contact in the database.

    :param body: ContactCreate: Get the data from the request body
    :param user: User: Get the user id from the token and use it to create a new contact
    :param db: Session: Access the database

    :return: A contact object

    :doc-author: Trelent
    """
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_data=body.additional_data,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(
        contact_id: int, user: User, db: Session
) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact.
            db (Session): A session object for interacting with the database.

    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user id from the database
    :param db: Session: Access the database

    :return: The contact object that was deleted

    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(
        contact_id: int, body: ContactUpdate, user: User, db: Session
) -> Contact | None:
    """
    The update_contact function updates a contact in the database.

    :param contact_id: int: Identify the contact to be updated
    :param body: ContactUpdate: Pass in the updated contact information
    :param user: User: Get the user_id from the logged-in user
    :param db: Session: Access the database

    :return: The updated contact, or none if the contact was not found

    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        for field, value in body.dict().items():
            setattr(contact, field, value)
        db.commit()
    return contact


async def search_contacts(
    db: Session, first_name: str = "", last_name: str = "", email: str = ""
) -> list[Type[Contact]]:
    """
    The search_contacts function searches for contacts in the database.

    :param db: Session: Pass in the database session
    :param first_name: str: Filter the first name of a contact
    :param last_name: str: Filter the contacts by last name
    :param email: str: Search for contacts by email

    :return: A list of contact objects

    :doc-author: Trelent
    """
    return db.query(Contact).filter(
        and_(
            Contact.first_name.ilike(f"%{first_name}%"),
            Contact.last_name.ilike(f"%{last_name}%"),
            Contact.email.ilike(f"%{email}%"),
            Contact.user_id == User.id,
        )
    ).all()


async def get_contacts_upcoming_birthdays(
        db: Session
) -> list[Type[Contact]]:
    """
    The get_contacts_upcoming_birthdays function returns a list of contacts
    whose birthdays are within the next week.

    :param db: Session: Pass in the database session

    :return: A list of contacts

    :doc-author: Trelent
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    return db.query(Contact).filter(
        and_(
            Contact.birthday is not None,
            func.date_part(
                'month', Contact.birthday
            ) == func.date_part('month', today),
            func.date_part(
                'day', Contact.birthday
            ) >= func.date_part('day', today),
            func.date_part(
                'day', Contact.birthday
            ) <= func.date_part('day', next_week),
            Contact.user_id == User.id
        )
    ).all()
