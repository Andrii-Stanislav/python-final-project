from typing import List
from src.models.address_book import AddressBook


def handle_add_address(args: List[str], book: AddressBook) -> str:
    """Add an address to an existing contact.
    
    This function interactively collects address information from the user,
    including street, city, region, and post-index. Each field is validated
    before being added to the contact's record.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message containing the added address information.
        
    Raises:
        ValueError: If contact name is not provided or contact is not found.
        ValueError: If address already exists for the contact.
    """
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    name, *_ = args 
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    elif record.address:
        raise ValueError(f"Address already exists for {name}")
    address_parts = []
    address_fields = ["Street", "City", "Region", "Post-index"]
    for field in address_fields:
        value = input(f"Enter {field}: ")
        if not value.strip():
            raise ValueError(f"{field} cannot be empty.")
        if field == "Post-index" and not value.isdigit():
            raise ValueError("Post-index must contain only digits.")
        address_parts.append(value)
    record.add_address(address_parts)
    return f"Address: {' '.join(address_parts)} added for {name}"

def handle_show_address(args: List[str], book: AddressBook) -> None:
    """Display the address of a given contact.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to search in.
    
    Returns:
        None: Prints the address information to the console.
        
    Raises:
        ValueError: If contact name is not provided or contact is not found.
    """
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    name, *_ = args 
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    return record.show_address()

def handle_delete_address(args: List[str], book: AddressBook) -> None:
    """Delete the address of a given contact.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        None: Removes the address from the contact's record.
        
    Raises:
        ValueError: If contact name is not provided or contact is not found.
    """
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    name, *_ = args 
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    return record.delete_address()