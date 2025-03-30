from src.models.address_book import AddressBook
from colorama import Fore, Style


def handle_add_contact(args_str: str, book: AddressBook) -> str:
    """Add a new contact with a name and an optional phone number.
    
    Args:
        args_str (str): String containing contact name and phone number.
                         The last element should be the phone number, all previous elements form the name.
                         Example: "John Smith: 1234567890"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if contact was added successfully.
        
    Raises:
        ValueError: If contact name or phone number is not provided.
        Exception: If there's an error adding the contact.
    """
    args = args_str.split() if args_str else []
    
    if not args:
        raise ValueError("Please provide contact name and phone number.")
    if len(args) < 2:
        raise IndexError("Please provide at least one contact name and a phone number.")

    phone = args[-1]  # Last argument as phone number
    name = " ".join(args[:-1])  # Join all but the last argument as the contact name

    # Normalize name using the AddressBook method
    name = book.normalize_name(name)

    try:
        result = book.add_contact(name, phone)
        return result
    except Exception as e:
        return f"Error adding {name}: {str(e)}"

def add_email_to_contact(args_str: str, book: AddressBook) -> str:
    """Add an email address to an existing contact.
    
    Args:
        args_str (str): String containing contact name and email address.
                         The last element should be the email, all previous elements form the name.
                         Example: "John Smith: john@example.com"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if email was added successfully.
        
    Raises:
        ValueError: If contact name or email address is not provided.
        KeyError: If contact is not found in the address book.
    """
    if not args_str.strip():
        raise ValueError("Please provide contact name and email address.")
    
    args = args_str.split(':') if args_str else []
    
    if len(args) != 2:
        raise ValueError("Please provide contact name and email address.")
    
    name = args[0].strip() if args[0] else ""
    email = args[1].strip() if args[1] else ""
    
    if not name or not email:
        raise ValueError("Please provide contact name and email address.")

    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        raise KeyError(f"Contact '{name}' not found.")

    record.add_email(email.strip())
    return "Email added."

def handle_change_contact(args_str: str, book: AddressBook) -> str:
    """Change a contact's phone number for multiple contacts.
    
    Args:
        args_str (str): String containing contact name, current phone number, and new phone number.
                         The last two elements should be the old and new phone numbers,
                         all previous elements form the name.
                         Example: "John Smith: 1234567890: 0987654321"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if phone number was changed successfully.
        
    Raises:
        ValueError: If contact name, current phone, or new phone is not provided.
        Exception: If there's an error changing the contact's phone number.
    """
            
    args = args_str.split(':') if args_str else [None, '']
    
    if len(args) != 2:
        raise ValueError("Please provide contact name, current phone number, and new phone number.")
    
    name = args[0].strip() if args[0] else ""
    phones = args[1].strip() if args[1] else ""
    
    if not name or not phones:
        raise ValueError("Please provide contact name, current phone number, and new phone number.")

    [old_phone, new_phone] = phones.split()
    name = book.normalize_name(name)

    return book.change_contact(name, old_phone.strip(), new_phone.strip())

def handle_show_phone(args_str: str, book: AddressBook) -> str:
    """Show the phone number(s) for a given contact.
    
    Args:
        args_str (str): String containing the contact name.
                         Example: "John Smith"
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's phone number(s).
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    name = args_str.strip()
    
    if not name:
        raise ValueError("Please provide contact name.")
    
    name = book.normalize_name(name)
    try:
        return book.show_phone(name)
    except KeyError:
        raise KeyError(f"Contact '{name}' not found.")

def handle_show_email(args_str: str, book: AddressBook) -> str:
    """Show the email address for a given contact.
    
    Args:
        args_str (str): String containing the contact name.
                         Example: "John Smith"
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's email address.
        
    Raises:
        IndexError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    name = args_str.strip()
    
    if not name:
        raise IndexError("Please provide contact name.")

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

def handle_delete_contact(args_str: str, book: AddressBook) -> str:
    """Delete a contact by name.
    
    Args:
        args_str (str): String containing the contact name.
                         Example: "John Smith"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if contact was deleted successfully.
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    name = args_str.strip()
    
    if not name:
        raise ValueError("Please provide the name of the contact to delete.")

    name = book.normalize_name(name)
    try:
        book.delete(name)
        return f"{Fore.GREEN}Contact '{name}' has been deleted.{Style.RESET_ALL}"
    except KeyError:
        raise ValueError(f"Contact '{name}' not found.")

def handle_find_contact(args_str: str, book: AddressBook) -> str:
    """Find contacts by name.
    
    Args:
        args_str (str): String containing the search keyword.
                         Example: "John Smith"
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's information.
        
    Raises:
        IndexError: If search keyword is not provided.
    """
    name = args_str.strip()
    
    if not name:
        raise IndexError("Please provide a search keyword.")
    
    name = book.normalize_name(name)

    found_contacts = book.find_contacts(name)

    if not found_contacts:
        raise KeyError("No matching contacts found.")

    return '\n'.join(str(record) for record in found_contacts)