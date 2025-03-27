"""PYTHONPATH=$PYTHONPATH:. python -m unittest discover -s tests"""

import unittest
from datetime import datetime, timedelta
from src.models.address_book import AddressBook
from src.models.record import Record


class TestAddressBookCommands(unittest.TestCase):
    def setUp(self):
        """Create a new AddressBook instance with sample data for each test."""
        self.book = AddressBook()

        # Contact 1: Multi-word name with phone
        jose = Record("Jose Maria Carrero")
        jose.add_phone("0116538866")
        self.book.add_record(jose)

        # Contact 2: Multi-word name with multiple phones, email
        ron = Record("Ron Whisley")
        ron.add_phone("0117775522")
        ron.add_phone("0117775511")
        ron.add_email("ron@mail.co.uk")
        self.book.add_record(ron)

    def test_add_contact(self):
        """Test adding a new contact with a phone number."""
        result = self.book.add_contact("New Contact", "0123456789")
        self.assertEqual(result, "Contact added.")
        record = self.book.find("New Contact")
        self.assertIsNotNone(record)
        self.assertEqual(len(record.phones), 1)
        self.assertEqual(record.phones[0].value, "0123456789")

    def test_add_contact_existing(self):
        """Test adding a phone to an existing contact."""
        result = self.book.add_contact("Jose Maria Carrero", "0116538852")
        self.assertEqual(result, "Contact updated.")
        record = self.book.find("Jose Maria Carrero")
        self.assertEqual(len(record.phones), 2)
        self.assertIn("0116538852", [phone.value for phone in record.phones])

    def test_add_birthday(self):
        """Test adding a birthday to an existing contact."""
        record = self.book.find("Jose Maria Carrero")
        record.add_birthday("31.03.1979")
        self.assertEqual(record.birthday.value.strftime("%d.%m.%Y"), "31.03.1979")

    def test_show_birthday(self):
        """Test showing a contact's birthday."""
        record = self.book.find("Ron Whisley")
        record.add_birthday("25.09.1960")
        birthday = record.show_birthday()
        self.assertEqual(birthday, "25.09.1960")

    def test_show_birthday_none(self):
        """Test showing birthday when none is set."""
        record = self.book.find("Jose Maria Carrero")
        self.assertIsNone(record.birthday)
        with self.assertRaises(ValueError) as context:
            record.show_birthday()
        self.assertEqual(str(context.exception), "Birthday not set.")

    def test_show_email(self):
        """Test showing a contact's email."""
        record = self.book.find("Ron Whisley")
        self.assertEqual(record.show_email(), "ron@mail.co.uk")

    def test_show_email_none(self):
        """Test showing email when none is set."""
        record = self.book.find("Jose Maria Carrero")
        self.assertIsNone(record.email)
        with self.assertRaises(ValueError) as context:
            record.show_email()
        self.assertEqual(str(context.exception), "No email set for the contact.")

    def test_invalid_contact(self):
        """Test finding a nonexistent contact."""
        self.assertIsNone(self.book.find("Nonexistent Contact"))

    def test_change_contact(self):
        """Test changing a contact's phone number."""
        result = self.book.change_contact("Ron Whisley", "0117775522", "0117775533")
        self.assertEqual(result, "Phone number updated.")
        record = self.book.find("Ron Whisley")
        phones = [phone.value for phone in record.phones]
        self.assertIn("0117775533", phones)
        self.assertNotIn("0117775522", phones)

    def test_change_contact_invalid_phone(self):
        """Test changing a non-existent phone number."""
        with self.assertRaises(ValueError) as context:
            self.book.change_contact("Ron Whisley", "9999999999", "0117775533")
        self.assertEqual(
            str(context.exception), "Phone number 9999999999 not found for editing."
        )

    def test_add_email(self):
        """Test adding an email to an existing contact."""
        result = self.book.add_email_to_contact("Jose Maria Carrero", "jose@mail.com")
        self.assertEqual(result, "Contact updated with email address.")
        record = self.book.find("Jose Maria Carrero")
        self.assertEqual(record.email.value, "jose@mail.com")

    def test_show_all(self):
        """Test showing all contacts."""
        expected_lines = [
            "Contact name: Jose Maria Carrero, phone(s): 0116538866",
            "Contact name: Ron Whisley, phone(s): 0117775522; 0117775511, email: ron@mail.co.uk",
        ]
        actual_output = self.book.show_all().split("\n")
        self.assertEqual(len(actual_output), 2)
        for expected, actual in zip(expected_lines, actual_output):
            self.assertEqual(actual.strip(), expected.strip())

    def test_show_all_with_birthday(self):
        """Test showing all contacts with a birthday added."""
        self.book.find("Jose Maria Carrero").add_birthday("31.03.1979")
        expected_lines = [
            "Contact name: Jose Maria Carrero, phone(s): 0116538866, birthday: 31.03.1979",
            "Contact name: Ron Whisley, phone(s): 0117775522; 0117775511, email: ron@mail.co.uk",
        ]
        actual_output = self.book.show_all().split("\n")
        self.assertEqual(len(actual_output), 2)
        for expected, actual in zip(expected_lines, actual_output):
            self.assertEqual(actual.strip(), expected.strip())

    def test_upcoming_birthdays(self):
        """Test getting upcoming birthdays with weekend adjustment."""
        today = datetime.now().date()
        future_date = today + timedelta(days=3)  # e.g., 30.03.2025 if today is 27.03
        future_date_str = future_date.strftime("%d.%m.%Y")
        self.book.find("Ron Whisley").add_birthday(future_date_str)

        upcoming = self.book.get_upcoming_birthdays()
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0]["name"], "Ron Whisley")

        # Adjust for weekend shift
        expected_date = future_date
        if future_date.weekday() == 5:  # Saturday
            expected_date += timedelta(days=2)
        elif future_date.weekday() == 6:  # Sunday
            expected_date += timedelta(days=1)
        expected_date_str = expected_date.strftime("%d.%m.%Y")
        self.assertEqual(upcoming[0]["birthday"], expected_date_str)

    def test_delete_contact(self):
        """Test deleting a contact."""
        self.book.delete("Ron Whisley")
        self.assertIsNone(self.book.find("Ron Whisley"))
        self.assertEqual(len(self.book.data), 1)


if __name__ == "__main__":
    unittest.main()
