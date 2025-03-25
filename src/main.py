from src.utils.storage import load_data, save_data
from src.utils.input_parser import parse_input
from src.handlers.contact_handlers import (
    handle_add_contact,
    handle_change_contact,
    handle_show_phone,
    handle_show_all
)
from src.handlers.birthday_handlers import (
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays
)
from src.handlers.note_handlers import ( 
    handle_add_note,
    handle_edit_note,
    handle_delete_note,
    handle_show_notes,
    handle_find_note
)
from src.models.address_book import AddressBook
from src.models.notes_book import NotesBook  

def main() -> None:
    filename: str = "my_address_book.pkl"
    notes_filename: str = "my_notes.pkl"

    book: AddressBook = load_data(filename)
    notes: NotesBook = load_data(notes_filename) 
    
    print("Welcome to the assistant bot!")

    while True:
        user_input: str = input("Enter a command: ")
        command: str
        args: list[str]
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book, filename)
            save_data(notes, notes_filename) 
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(handle_add_contact(args, book))

        elif command == "change":
            print(handle_change_contact(args, book))

        elif command == "phone":
            print(handle_show_phone(args, book))

        elif command == "all":
            print(handle_show_all(book))

        elif command == "add-birthday":
            print(handle_add_birthday(args, book))

        elif command == "show-birthday":
            print(handle_show_birthday(args, book))

        elif command == "birthdays":
            print(handle_birthdays(args, book))

        # Notes
        elif command == "add-note":
            print(handle_add_note(args, notes))

        elif command == "edit-note":
            print(handle_edit_note(args, notes))

        elif command == "delete-note":
            print(handle_delete_note(args, notes))

        elif command == "find-note":
            print(handle_find_note(args, notes))

        elif command == "show-notes":
            print(handle_show_notes(notes))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
