import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    search_contacts,
    get_contacts_upcoming_birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_note_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactCreate(
            first_name="first_name",
            last_name="last_name",
            email="email",
            phone_number="phone_number"
        )

        result = await create_contact(
            body=body, user=self.user, db=self.session
        )
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact = Contact()
        body = ContactUpdate(
            first_name="first_name",
            last_name="last_name",
            email="email",
            phone_number="phone_number",
            done=True
        )
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1, body=body, user=self.user, db=self.session
        )
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(
            first_name="first_name",
            last_name="last_name",
            email="email",
            phone_number="phone_number",
            done=True
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1, body=body, user=self.user, db=self.session
        )
        self.assertIsNone(result)

    async def test_search_contacts_found(self):
        first_name = "first_name_"
        last_name = "last_name_"
        email = "email_"
        contacts_found = [
            Contact(
                first_name="first_name_1",
                last_name="last_name_1",
                email="email_1",
                phone_number="phone_number_1",
            ),
            Contact(
                first_name="first_name_2",
                last_name="last_name_2",
                email="email_2",
                phone_number="phone_number_2",
            ),
        ]
        self.session.query().filter(
            and_(
                Contact.first_name.ilike(f"%{first_name}%"),
                Contact.last_name.ilike(f"%{last_name}%"),
                Contact.email.ilike(f"%{email}%"),
                Contact.user_id == User.id,
            )
        ).all.return_value = contacts_found
        result = await search_contacts(
            first_name="first_name_",
            last_name="last_name_",
            email="email_",
            db=self.session
        )
        self.assertEqual(result, contacts_found)

    async def test_search_contacts_not_found(self):
        first_name = "first_name_3"
        last_name = "last_name_3"
        email = "email_3"
        contacts_found = [
            Contact(
                first_name="first_name_1",
                last_name="last_name_1",
                email="email_1",
                phone_number="phone_number_1",
            ),
            Contact(
                first_name="first_name_2",
                last_name="last_name_2",
                email="email_2",
                phone_number="phone_number_2",
            ),
        ]
        self.session.query().filter(
            and_(
                Contact.first_name.ilike(f"%{first_name}%"),
                Contact.last_name.ilike(f"%{last_name}%"),
                Contact.email.ilike(f"%{email}%"),
                Contact.user_id == User.id,
            )
        ).all.return_value = None
        result = await search_contacts(
            first_name="first_name_",
            last_name="last_name_",
            email="email_",
            db=self.session
        )
        self.assertEqual(result, None)

    async def test_get_contacts_upcoming_birthdays_found(self):
        contacts = [
            Contact(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                birthday=datetime.now().date() + timedelta(days=2),
                user_id=1
            ),
            Contact(
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                birthday=datetime.now().date() + timedelta(days=5),
                user_id=1
            )
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_upcoming_birthdays(db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_upcoming_birthdays_not_found(self):
        data = self.session.query().filter().all.return_value = None
        result = await get_contacts_upcoming_birthdays(db=self.session)
        self.assertEqual(result, data)


if __name__ == '__main__':
    unittest.main()

