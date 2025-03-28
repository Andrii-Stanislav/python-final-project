from src.models.address_book import AddressBook
from src.models.notes_book import NotesBook
from src.utils.storage import load_data, save_data
from src.handlers.contact_handlers import (
    handle_add_contact,
    handle_show_all,
    handle_show_phone,
    handle_delete_contact,
    add_email_to_contact,
    handle_change_contact,
)
from src.handlers.address_handlers import handle_add_address
from src.handlers.note_handlers import (
    handle_add_note,
    handle_show_notes,
    handle_find_note,
    handle_edit_note,
    handle_delete_note,
)
from src.handlers.birthday_handlers import (
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays,
)
from src.ui.terminal_ui import TerminalUI

def main():
    address_book = load_data("my_address_book.pkl", AddressBook)
    notes_book = load_data("my_notes.pkl", NotesBook)

    # Create a dictionary of handlers
    handlers = {
        # Contact handlers
        "Add Contact": lambda args: handle_add_contact(args, address_book),
        "Show All Contacts": lambda args: handle_show_all(address_book),
        "Find Contact": lambda args: handle_show_phone(args, address_book),
        "Delete Contact": lambda args: handle_delete_contact(args, address_book),
        "Add Email": lambda args: add_email_to_contact(args, address_book),
        "Change Phone": lambda args: handle_change_contact(args, address_book),
        "Add Address": lambda args: handle_add_address(args, address_book),
        
        # Note handlers
        "Add Note": lambda args: handle_add_note(args, notes_book),
        "Show All Notes": lambda args: handle_show_notes(notes_book),
        "Find Note": lambda args: handle_find_note(args, notes_book),
        "Edit Note": lambda args: handle_edit_note(args, notes_book),
        "Delete Note": lambda args: handle_delete_note(args, notes_book),
        
        # Birthday handlers
        "Add Birthday": lambda args: handle_add_birthday(args, address_book),
        "Show Birthday": lambda args: handle_show_birthday(args, address_book),
        "Show Upcoming Birthdays": lambda args: handle_birthdays(args, address_book),
    }

    # Create and run the UI
    ui = TerminalUI()
    ui.run(handlers)

    save_data(address_book, "my_address_book.pkl")
    save_data(notes_book, "my_notes.pkl")

if __name__ == "__main__":
    main()
