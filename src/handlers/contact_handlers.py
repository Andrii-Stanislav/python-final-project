from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook


@input_error
def handle_add_contact(args: List[str], book: AddressBook) -> str:
    """Add a new contact with a name and one phone number. Handler accepts the naming format: first name, middle name, last name, prefixes, related symbols, and even lowercase input"""
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


@input_error
def add_email_to_contact(args: List[str], book: AddressBook) -> str:
    """Add an email to an existing contact."""
    if len(args) < 2:
        raise IndexError("Please provide contact name and email address.")

    email = args[-1]
    name = " ".join(args[:-1])
    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        raise KeyError(f"Contact '{name}' not found.")

    record.add_email(email)
    return "Email added."


@input_error
def handle_change_contact(args: List[str], book: AddressBook) -> str:
    """Change a contact's phone number."""
    if len(args) < 3:
        raise IndexError(
            "Please provide contact name, current phone number, and new phone number."
        )

    old_phone = args[-2]
    new_phone = args[-1]
    name = " ".join(args[:-2])
    name = book.normalize_name(name)

    return book.change_contact(name, old_phone, new_phone)


@input_error
def handle_show_phone(args: List[str], book: AddressBook) -> str:
    """Show the phone number(s) for a given contact."""
    if not args:
        raise IndexError("Please provide contact name.")
    name = " ".join(args)
    name = book.normalize_name(name)

    return book.show_phone(name)


@input_error
def handle_show_email(args: List[str], book: AddressBook) -> str:
    """Show the email address for a given contact."""
    if not args:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    return book.show_email(name)


@input_error
def handle_show_all(book: AddressBook) -> str:
    """Show all contacts in the address book."""
    try:
        return book.show_all()
    except ValueError as e:
        return f"Error: {e}"


@input_error
def handle_delete_contact(args: List[str], book: AddressBook) -> str:
    """Delete a contact by name."""
    if len(args) < 1:
        raise ValueError("Please provide the name of the contact to delete.")

    name = " ".join(args)
    name = book.normalize_name(name)
    try:
        book.delete(name)
        return f"Contact '{name}' has been deleted."
    except KeyError as e:
        return str(e)
    
    
@input_error
def handle_find_contact(args: List[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise IndexError("Please provide a search keyword.")
    
    found_contacts = book.find_contacts(args[0])

    if not found_contacts:
        return "No matching contacts found."

    return '\n'.join(str(record) for record in found_contacts)
