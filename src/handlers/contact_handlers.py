from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook


@input_error
def handle_add_contact(args: List[str], book: AddressBook) -> str:
    """Add a new contact with a name and an optional phone number."""
    if len(args) != 2:
        raise IndexError("Please provide contact name and a phone number.")
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    return book.add_contact(name, phone)


@input_error
def handle_add_email(args: List[str], book: AddressBook) -> str:
    """Add an email address to an existing contact."""
    if len(args) != 2:
        raise IndexError("Please provide contact name and email address.")
    name = args[0]
    email = args[1]
    return book.add_email_to_contact(name, email)


@input_error
def handle_change_contact(args: List[str], book: AddressBook) -> str:
    """Change a contact's phone number."""
    if len(args) != 3:
        raise IndexError(
            "Please provide contact name, old phone number and new phone number."
        )
    name, old_phone, new_phone = args
    return book.change_contact(name, old_phone, new_phone)


@input_error
def handle_show_phone(args: List[str], book: AddressBook) -> str:
    """Show the phone number(s) for a given contact."""
    if len(args) != 1:
        raise IndexError("Please provide contact name.")
    name = args[0]
    return book.show_phone(name)


@input_error
def handle_show_email(args: List[str], book: AddressBook) -> str:
    """Show the email address for a given contact."""
    if len(args) != 1:
        raise IndexError("Please provide contact name.")
    name = args[0]
    return book.show_email(name)


@input_error
def handle_show_all(book: AddressBook) -> str:
    """Show all contacts in the address book."""
    return book.show_all()
