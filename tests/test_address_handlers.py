import pytest
from src.models.address_book import AddressBook
from src.handlers.address_handlers import (
    handle_add_address,
    handle_show_address,
    handle_delete_address
)

@pytest.fixture
def address_book():
    return AddressBook()

def test_handle_add_address(address_book):
    # First add a contact
    address_book.add_contact("John Smith", "1234567890")
    
    # Test adding address
    result = handle_add_address("John Smith: 123 Main St, Anytown, USA, 12345", address_book)
    assert "Address:  123 Main St  Anytown  USA  12345 added for John Smith" in result
    
    # Test adding address to non-existent contact
    with pytest.raises(ValueError):
        handle_add_address("Jane Doe: 123 Main St, Anytown, USA, 12345", address_book)
    
    # Test adding address with invalid format
    with pytest.raises(ValueError):
        handle_add_address("John Smith: 123 Main St", address_book)
    
    # Test adding address when address already exists
    with pytest.raises(ValueError):
        handle_add_address("John Smith: 456 Oak St, Somewhere, USA, 67890", address_book)

def test_handle_show_address(address_book):
    # First add a contact with address
    address_book.add_contact("John Smith", "1234567890")
    handle_add_address("John Smith: 123 Main St, Anytown, USA, 12345", address_book)
    
    # Test showing address
    result = handle_show_address("John Smith", address_book)
    assert "123 Main St" in result
    assert "Anytown" in result
    assert "USA" in result
    assert "12345" in result
    
    # Test showing address for non-existent contact
    with pytest.raises(ValueError):
        handle_show_address("Jane Doe", address_book)
    
    # Test showing address with empty input
    with pytest.raises(IndexError):
        handle_show_address("", address_book)

def test_handle_delete_address(address_book):
    # First add a contact with address
    address_book.add_contact("John Smith", "1234567890")
    handle_add_address("John Smith: 123 Main St, Anytown, USA, 12345", address_book)
    
    # Test deleting address
    result = handle_delete_address("John Smith", address_book)
    assert "The address has been removed for John Smith" in result
    
    # Test deleting address for non-existent contact
    with pytest.raises(ValueError):
        handle_delete_address("Jane Doe", address_book)
    
    # Test deleting address with empty input
    with pytest.raises(ValueError):
        handle_delete_address("", address_book) 