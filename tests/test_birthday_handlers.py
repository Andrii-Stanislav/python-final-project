import pytest
from src.models.address_book import AddressBook
from src.handlers.birthday_handlers import (
    handle_add_birthday,
    handle_show_birthday,
    handle_delete_birthday,
    handle_birthdays
)
from src.models.fields import ValidationException

@pytest.fixture
def address_book():
    return AddressBook()

def test_handle_add_birthday(address_book):
    # First add a contact
    address_book.add_contact("John Smith", "1234567890")
        
    # Test adding birthday
    result = handle_add_birthday("John Smith: 01.01.2000", address_book)
    assert "Birthday added" in result
    
    # Test adding birthday to non-existent contact
    with pytest.raises(KeyError):
        result = handle_add_birthday("Jane Doe: 01.01.2000", address_book)
        assert "Contact 'Jane Doe' not found" in result

    # Test adding birthday with invalid date format
    with pytest.raises(ValidationException):
        result = handle_add_birthday("John Smith: invalid-date", address_book)
        assert "Invalid date format. Use DD.MM.YYYY" in result

def test_handle_show_birthday(address_book):
    # First add a contact with birthday
    address_book.add_contact("John Smith", "1234567890")
    handle_add_birthday("John Smith: 01.01.2000", address_book)
    
    # Test showing birthday
    result = handle_show_birthday("John Smith", address_book)
    assert "01.01.2000" in result
    
    # Test showing birthday for non-existent contact
    with pytest.raises(KeyError):
        handle_show_birthday("Jane Doe", address_book)
    
    # Test showing birthday for contact without birthday
    address_book.add_contact("Jane Doe", "0987654321")
    with pytest.raises(ValueError):
        handle_show_birthday("Jane Doe", address_book)

def test_handle_delete_birthday(address_book):
    # First add a contact with birthday
    address_book.add_contact("John Smith", "1234567890")
    handle_add_birthday("John Smith: 01.01.2000", address_book)
    
    # Test deleting birthday
    result = handle_delete_birthday("John Smith", address_book)
    assert "The birthday has been removed for John Smith" in result
    
    # Test deleting birthday for non-existent contact
    with pytest.raises(IndexError):
        handle_delete_birthday("Jane Doe", address_book)

def test_handle_birthdays(address_book):
    # First add some contacts with birthdays
    address_book.add_contact("John Smith", "1234567890")
    handle_add_birthday("John Smith: 01.01.2000", address_book)
    address_book.add_contact("Jane Doe", "0987654321")
    handle_add_birthday("Jane Doe: 15.01.2000", address_book)
    
    # Test showing upcoming birthdays
    result = handle_birthdays("365", address_book)
    assert "Name" in result
    assert "Birthday" in result
    assert "Congratulation day" in result
    
    # Test showing upcoming birthdays with invalid input
    with pytest.raises(ValueError):
        handle_birthdays("", address_book)
    
    # Test showing upcoming birthdays when no birthdays in range
    with pytest.raises(ValueError):
        handle_birthdays("1", address_book) 