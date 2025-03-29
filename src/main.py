# Unused features because of "Terminal UI" implementation
# from src.utils.command_suggestions import suggest_command
# from src.utils.command_help import get_help_table

from src.utils.storage import load_data, save_data
from src.models.address_book import AddressBook
from src.models.notes_book import NotesBook

from src.handlers.contact_handlers import (
    handle_add_contact,
    handle_show_all,
    handle_show_phone,
    handle_delete_contact,
    add_email_to_contact,
    handle_change_contact,
    handle_show_phone,
    handle_show_email,
    handle_find_contact,
)
from src.handlers.address_handlers import (
    handle_add_address,
    handle_show_address,
    handle_delete_address
)
from src.handlers.note_handlers import (
    handle_add_note,
    handle_show_notes,
    handle_find_note,
    handle_edit_note,
    handle_delete_note,
    handle_add_tag,
    handle_remove_tag,
    handle_check_tag,
    handle_find_notes_by_tag,
)
from src.handlers.birthday_handlers import (
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays,
    handle_delete_birthday,
)
from src.ui.terminal_ui import TerminalUI
from src.handlers.address_handlers import (
    handle_add_address,
    handle_show_address,
    handle_delete_address
)
from src.handlers.note_handlers import ( 
    handle_add_note,
    handle_edit_note,
    handle_delete_note,
    handle_show_notes,
    handle_find_note,
    handle_add_tag,
    handle_remove_tag,
    handle_check_tag,
    handle_find_notes_by_tag,
)

ADDRESS_BOOK_NAME = "my_address_book.pkl"
NOTES_BOOK_NAME = "my_notes.pkl"

def wrap_handler(handler, address_book=None, notes_book=None):
    """Wrapper function to save data after handler execution."""
    def wrapped_handler(args):
        result = handler(args)
        if address_book:
            save_data(address_book, ADDRESS_BOOK_NAME)
        if notes_book:
            save_data(notes_book, NOTES_BOOK_NAME)
        return result
    return wrapped_handler

def main():
    address_book = load_data("my_address_book.pkl", AddressBook)
    notes_book = load_data("my_notes.pkl", NotesBook)

    # Create a dictionary of handlers
    handlers = {
        # Contact handlers
        "Add Contact": wrap_handler(lambda args: handle_add_contact(args, address_book), address_book=address_book),
        "Show All Contacts": wrap_handler(lambda args: handle_show_all(address_book), address_book=address_book),
        "Find Contact": wrap_handler(lambda args: handle_show_phone(args, address_book), address_book=address_book),
        "Delete Contact": wrap_handler(lambda args: handle_delete_contact(args, address_book), address_book=address_book),
        "Add Email": wrap_handler(lambda args: add_email_to_contact(args, address_book), address_book=address_book),
        "Change Phone": wrap_handler(lambda args: handle_change_contact(args, address_book), address_book=address_book),
        "Show Email": wrap_handler(lambda args: handle_show_email(args, address_book), address_book=address_book),
        "Search Contact": wrap_handler(lambda args: handle_find_contact(args, address_book), address_book=address_book),
        
        # Address handlers
        "Add Address": wrap_handler(lambda args: handle_add_address(args, address_book), address_book=address_book),
        "Show Address": wrap_handler(lambda args: handle_show_address(args, address_book), address_book=address_book),
        "Delete Address": wrap_handler(lambda args: handle_delete_address(args, address_book), address_book=address_book),
        
        # Note handlers
        "Add Note": wrap_handler(lambda args: handle_add_note(args, notes_book), notes_book=notes_book),
        "Show All Notes": wrap_handler(lambda args: handle_show_notes(notes_book), notes_book=notes_book),
        "Find Note": wrap_handler(lambda args: handle_find_note(args, notes_book), notes_book=notes_book),
        "Edit Note": wrap_handler(lambda args: handle_edit_note(args, notes_book), notes_book=notes_book),
        "Delete Note": wrap_handler(lambda args: handle_delete_note(args, notes_book), notes_book=notes_book),
        "Add Tag": wrap_handler(lambda args: handle_add_tag(args, notes_book), notes_book=notes_book),
        "Remove Tag": wrap_handler(lambda args: handle_remove_tag(args, notes_book), notes_book=notes_book),
        "Check Tag": wrap_handler(lambda args: handle_check_tag(args, notes_book), notes_book=notes_book),
        "Find Notes by Tag": wrap_handler(lambda args: handle_find_notes_by_tag(args, notes_book), notes_book=notes_book),
        
        # Birthday handlers
        "Add Birthday": wrap_handler(lambda args: handle_add_birthday(args, address_book), address_book=address_book),
        "Show Birthday": wrap_handler(lambda args: handle_show_birthday(args, address_book), address_book=address_book),
        "Show Upcoming Birthdays": wrap_handler(lambda args: handle_birthdays(args, address_book), address_book=address_book),
        "Delete Birthday": wrap_handler(lambda args: handle_delete_birthday(args, address_book), address_book=address_book),
    }

    # Create and run the UI
    ui = TerminalUI()
    ui.run(handlers)

    # Final save when exiting the program
    save_data(address_book, ADDRESS_BOOK_NAME)
    save_data(notes_book, NOTES_BOOK_NAME)

if __name__ == "__main__":
    main()
