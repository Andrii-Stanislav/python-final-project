from typing import List
from src.models.address_book import AddressBook


def handle_add_contact(args: List[str], book: AddressBook) -> str:
    """Add a new contact with a name and an optional phone number.
    
    Args:
        args (List[str]): List containing contact name and phone number.
                         The last element should be the phone number, all previous elements form the name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if contact was added successfully.
        
    Raises:
        ValueError: If contact name or phone number is not provided.
        Exception: If there's an error adding the contact.
    """
    if not args:
        raise ValueError("Please provide contact name and phone number.")
    if len(args) < 2:
        raise IndexError("Please provide at least one contact name and a phone number.")

    # TODO: edit validation for first_name, last_name, phone_number
    phone = args[-1]  # Last argument as phone number
    name = " ".join(args[:-1])  # Join all but the last argument as the contact name

    # Normalize name using the AddressBook method
    name = book.normalize_name(name)

    try:
        result = book.add_contact(name, phone)
        return result
    except Exception as e:
        return f"Error adding {name}: {str(e)}"

def add_email_to_contact(args: List[str], book: AddressBook) -> str:
    """Add an email address to an existing contact.
    
    Args:
        args (List[str]): List containing contact name and email address.
                         The last element should be the email, all previous elements form the name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if email was added successfully.
        
    Raises:
        ValueError: If contact name or email address is not provided.
        KeyError: If contact is not found in the address book.
    """
    if not args:
        raise ValueError("Please provide contact name and email address.")
    if len(args) < 2:
        raise IndexError("Please provide contact name and email address.")

    email = args[-1]
    name = " ".join(args[:-1])
    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        return f"Contact '{name}' not found."

    record.add_email(email)
    return "Email added."

def handle_change_contact(args: List[str], book: AddressBook) -> str:
    """Change a contact's phone number for multiple contacts.
    
    Args:
        args (List[str]): List containing contact name, current phone number, and new phone number.
                         The last two elements should be the old and new phone numbers,
                         all previous elements form the name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if phone number was changed successfully.
        
    Raises:
        ValueError: If contact name, current phone, or new phone is not provided.
        Exception: If there's an error changing the contact's phone number.
    """
    if not args:
        raise ValueError("Please provide contact name, current phone number, and new phone number.")
    if len(args) < 3:
        raise IndexError(
            "Please provide contact name, current phone number, and new phone number."
        )

    old_phone = args[-2]
    new_phone = args[-1]
    name = " ".join(args[:-2])
    name = book.normalize_name(name)

    return book.change_contact(name, old_phone, new_phone)

def handle_show_phone(args: List[str], book: AddressBook) -> str:
    """Show the phone number(s) for a given contact.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's phone number(s).
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    if not args:
        raise ValueError("Please provide contact name.")
    name = " ".join(args)
    name = book.normalize_name(name)
    try:
        return book.show_phone(name)
    except KeyError:
        return f"Contact '{name}' not found."

def handle_show_email(args: List[str], book: AddressBook) -> str:
    """Show the email address for a given contact.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's email address.
        
    Raises:
        IndexError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    if len(args) != 1:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    return book.show_email(name)

def handle_show_all(book: AddressBook) -> str:
    """Show all contacts in the address book.
    
    Args:
        book (AddressBook): The address book instance to display.
    
    Returns:
        str: Formatted string containing all contacts' information.
        
    Raises:
        ValueError: If there's an error retrieving the contacts.
    """
    try:
        return book.show_all()
    except ValueError as e:
        raise ValueError(f"Error: {e}")

def handle_delete_contact(args: List[str], book: AddressBook) -> str:
    """Delete a contact by name.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if contact was deleted successfully.
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    if not args:
        raise ValueError("Please provide the name of the contact to delete.")

    name = " ".join(args)
    name = book.normalize_name(name)
    try:
        book.delete(name)
        return f"Contact '{name}' has been deleted."
    except KeyError:
        raise ValueError(f"Contact '{name}' not found.")
