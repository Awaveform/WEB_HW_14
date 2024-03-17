from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:

    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Specify the email address of the user we want to retrieve
    :param db: Session: Pass the database session to the function

    :return: The first user with the email address that matches the provided parameter

    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:

    """
    The create_user function creates a new user in the database.
    Args:
        body (UserModel): The UserModel object containing the data to be added to the database.
        db (Session): The SQLAlchemy Session object used for querying and updating the database.

    :param body: UserModel: Create a new user object
    :param db: Session: Access the database

    :return: A user object

    :doc-author: Trelent
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user that is being updated
    :param token: str | None: Update the user's refresh token
    :param db: Session: Pass the database session to the function

    :return: None

    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:

    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function

    :return: None

    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:

    """
    The update_avatar function updates the avatar of a user in the database.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that is being passed in
    :param db: Session: Pass the database session to the function

    :return: The updated user

    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
