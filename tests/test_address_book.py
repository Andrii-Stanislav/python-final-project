import unittest
from src.models.address_book import AddressBook
from src.models.record import Record


"""Run your tests using the command line. For unittest, navigate to your project directory and run:\n
'PYTHONPATH=$PYTHONPATH:. python -m unittest discover -s tests'"""


class TestAddressBookCommands(unittest.TestCase):

    def setUp(self):
        """Create a new AddressBook instance for testing."""
        self.book = AddressBook()

        jose = Record("Jose Maria Carrero")
        jose.add_phone("0116538866")
        self.book.add_record(jose)

        ron = Record("Ron Whisley")
        ron.add_phone("0117775522")
        ron.add_phone("0117775511")
        ron.add_email("ron@mail.co.uk")
        self.book.add_record(ron)

    def test_add_contact(self):
        """Test adding a new contact."""
        new_contact = Record("New Contact")
        new_contact.add_phone("0123456789")
        result = self.book.add_record(new_contact)
        self.assertIsNotNone(self.book.find("New Contact"))

    def test_add_birthday(self):
        """Test adding a birthday to an existing contact."""
        self.book.find("Jose Maria Carrero").add_birthday("31.03.1979")
        birthday = self.book.find("Jose Maria Carrero").show_birthday()
        self.assertEqual(birthday, "31.03.1979")

    def test_show_birthday(self):
        """Test showing a birthday of a contact."""
        self.book.find("Jose Maria Carrero").add_birthday("31.03.1979")
        birthday = self.book.show_birthday("Jose Maria Carrero")
        self.assertIn("31.03.1979", birthday)

    def test_invalid_contact(self):
        """Test handling of an invalid contact."""
        with self.assertRaises(KeyError):
            self.book.find("Nonexistent Contact")

    def test_upcoming_birthdays(self):
        """Test getting upcoming birthdays."""
        self.book.find("Jose Maria Carrero").add_birthday("31.03.1979")
        upcoming = self.book.get_upcoming_birthdays()
        self.assertGreater(len(upcoming), 0)

    def test_show_all(self):
        """Test showing all contacts data."""
        expected_output = (
            "Contact name: Jose Maria Carrero, phone(s): 0116538866\n"
            "Contact name: Ron Whisley, phone(s): 0117775522; 0117775511, email: ron@mail.co.uk"
        )
        actual_output = self.book.show_all()
        self.assertEqual(actual_output.strip(), expected_output.strip())

    def test_add_email(self):
        """Test adding an email to an existing contact."""
        result = self.book.add_email_to_contact("Ron Whisley", "new_email@mail.com")
        self.assertEqual(result, "Email added.")
        record = self.book.find("Ron Whisley")
        self.assertIn("new_email@mail.com", record.emails)


if __name__ == "__main__":
    unittest.main()
