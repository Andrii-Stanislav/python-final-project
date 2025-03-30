import pytest
from src.models.address_book import AddressBook
from src.handlers.contact_handlers import (
    handle_add_contact,
    add_email_to_contact,
    handle_change_contact,
    handle_show_phone,
    handle_show_email,
    handle_show_all,
    handle_delete_contact,
    handle_find_contact
)

@pytest.fixture
def address_book():
    return AddressBook()

def test_handle_add_contact(address_book):
    # Test adding a contact with name and phone
    result = handle_add_contact("John Smith 1234567890", address_book)
    assert "Contact added" in result
    
    # Test adding a contact with invalid input
    with pytest.raises(ValueError):
        handle_add_contact("", address_book)
    
    with pytest.raises(IndexError):
        handle_add_contact("John", address_book)

def test_add_email_to_contact(address_book):
    # First add a contact
    handle_add_contact("John Smith 1234567890", address_book)
        
    # Test adding email
    result = add_email_to_contact("John Smith: john@gmail.com", address_book)
    assert "Email added." in result
    
    # Test adding email to non-existent contact
    with pytest.raises(KeyError):
        result = add_email_to_contact("Jane Doe: jane@gmail.com", address_book)
        assert "Contact 'Jane Doe' not found" in result

def test_handle_change_contact(address_book):
    # First add a contact
    handle_add_contact("John Smith 1234567890", address_book)
    
    # Test changing phone number
    result = handle_change_contact("John Smith: 1234567890 0987654321", address_book)
    assert "Phone number updated" in result
    
    # Test changing phone number for non-existent contact
    with pytest.raises(KeyError):
        result = handle_change_contact("Jane Doe: 1234567890 0987654321", address_book)
        assert "Contact 'Jane Doe' not found" in result

def test_handle_show_phone(address_book):
    # First add a contact
    handle_add_contact("John Smith 1234567890", address_book)
    
    # Test showing phone number
    result = handle_show_phone("John Smith", address_book)
    assert "1234567890" in result
    
    # Test showing phone for non-existent contact
    with pytest.raises(KeyError):
        result = handle_show_phone("Jane Doe", address_book)
        assert "Contact 'Jane Doe' not found" in result

def test_handle_show_email(address_book):
    # First add a contact with email
    handle_add_contact("John Smith 1234567890", address_book)
    add_email_to_contact("John Smith: john@gmail.com", address_book)
    
    # Test showing email
    result = handle_show_email("John Smith", address_book)
    assert "john@gmail.com" in result
    
    # Test showing email for non-existent contact
    with pytest.raises(KeyError):
        result = handle_show_email("Jane Doe", address_book)
        assert "Contact 'Jane Doe' not found" in result

def test_handle_show_all(address_book):
    # First add some contacts
    handle_add_contact("John Smith 1234567890", address_book)
    handle_add_contact("Jane Doe 0987654321", address_book)
    
    # Test showing all contacts
    result = handle_show_all(address_book)
    assert "John Smith" in result
    assert "Jane Doe" in result

def test_handle_delete_contact(address_book):
    # First add a contact
    handle_add_contact("John Smith 1234567890", address_book)
    
    # Test deleting contact
    result = handle_delete_contact("John Smith", address_book)
    assert "Contact 'John Smith' has been deleted" in result
    
    # Test deleting non-existent contact
    with pytest.raises(ValueError):
        handle_delete_contact("Jane Doe", address_book)

def test_handle_find_contact(address_book):
    # First add some contacts
    handle_add_contact("John Smith 1234567890", address_book)
    handle_add_contact("Johnny Doe 0987654321", address_book)
    
    # Test finding contacts
    result = handle_find_contact("John", address_book)
    assert "John Smith" in result
    assert "Johnny Doe" in result
    
    # Test finding non-existent contact
    with pytest.raises(KeyError):
        result = handle_find_contact("Jane", address_book)
        assert "No matching contacts found" in result 