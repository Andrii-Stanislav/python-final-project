# Unused features because of "Terminal UI" implementation
# from src.utils.command_suggestions import suggest_command
# from src.utils.command_help import get_help_table

from src.utils.storage import load_data, save_data
from src.models.address_book import AddressBook
from src.models.notes_book import NotesBook
from src.constants.commands import (
    ContactCommands,
    AddressCommands,
    NoteCommands,
    BirthdayCommands,
)

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
    '''
    Main function to run the address book and notes book.
    '''
    address_book = load_data("my_address_book.pkl", AddressBook)
    notes_book = load_data("my_notes.pkl", NotesBook)

    # Create a dictionary of handlers
    handlers = {
        # Contact handlers
        ContactCommands.ADD_CONTACT: wrap_handler(lambda args: handle_add_contact(args, address_book), address_book=address_book),
        ContactCommands.SHOW_ALL_CONTACTS: wrap_handler(lambda args: handle_show_all(address_book), address_book=address_book),
        ContactCommands.FIND_CONTACT: wrap_handler(lambda args: handle_show_phone(args, address_book), address_book=address_book),
        ContactCommands.DELETE_CONTACT: wrap_handler(lambda args: handle_delete_contact(args, address_book), address_book=address_book),
        ContactCommands.ADD_EMAIL: wrap_handler(lambda args: add_email_to_contact(args, address_book), address_book=address_book),
        ContactCommands.CHANGE_PHONE: wrap_handler(lambda args: handle_change_contact(args, address_book), address_book=address_book),
        ContactCommands.SHOW_EMAIL: wrap_handler(lambda args: handle_show_email(args, address_book), address_book=address_book),
        ContactCommands.SEARCH_CONTACT: wrap_handler(lambda args: handle_find_contact(args, address_book), address_book=address_book),
        
        # Address handlers
        AddressCommands.ADD_ADDRESS: wrap_handler(lambda args: handle_add_address(args, address_book), address_book=address_book),
        AddressCommands.SHOW_ADDRESS: wrap_handler(lambda args: handle_show_address(args, address_book), address_book=address_book),
        AddressCommands.DELETE_ADDRESS: wrap_handler(lambda args: handle_delete_address(args, address_book), address_book=address_book),
        
        # Note handlers
        NoteCommands.ADD_NOTE: wrap_handler(lambda args: handle_add_note(args, notes_book), notes_book=notes_book),
        NoteCommands.SHOW_ALL_NOTES: wrap_handler(lambda args: handle_show_notes(notes_book), notes_book=notes_book),
        NoteCommands.FIND_NOTE: wrap_handler(lambda args: handle_find_note(args, notes_book), notes_book=notes_book),
        NoteCommands.EDIT_NOTE: wrap_handler(lambda args: handle_edit_note(args, notes_book), notes_book=notes_book),
        NoteCommands.DELETE_NOTE: wrap_handler(lambda args: handle_delete_note(args, notes_book), notes_book=notes_book),
        NoteCommands.ADD_TAG: wrap_handler(lambda args: handle_add_tag(args, notes_book), notes_book=notes_book),
        NoteCommands.REMOVE_TAG: wrap_handler(lambda args: handle_remove_tag(args, notes_book), notes_book=notes_book),
        NoteCommands.CHECK_TAG: wrap_handler(lambda args: handle_check_tag(args, notes_book), notes_book=notes_book),
        NoteCommands.FIND_NOTES_BY_TAG: wrap_handler(lambda args: handle_find_notes_by_tag(args, notes_book), notes_book=notes_book),
        
        # Birthday handlers
        BirthdayCommands.ADD_BIRTHDAY: wrap_handler(lambda args: handle_add_birthday(args, address_book), address_book=address_book),
        BirthdayCommands.SHOW_BIRTHDAY: wrap_handler(lambda args: handle_show_birthday(args, address_book), address_book=address_book),
        BirthdayCommands.SHOW_UPCOMING_BIRTHDAYS: wrap_handler(lambda args: handle_birthdays(args, address_book), address_book=address_book),
        BirthdayCommands.DELETE_BIRTHDAY: wrap_handler(lambda args: handle_delete_birthday(args, address_book), address_book=address_book),
    }

    # Create and run the UI
    ui = TerminalUI()
    ui.run(handlers)

    # Final save when exiting the program
    save_data(address_book, ADDRESS_BOOK_NAME)
    save_data(notes_book, NOTES_BOOK_NAME)
