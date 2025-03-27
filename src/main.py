from src.utils.storage import load_data, save_data
from src.utils.input_parser import parse_input
from src.utils.command_suggestions import suggest_command
from src.utils.command_help import get_help_table
from src.handlers.contact_handlers import (
    handle_add_contact,
    handle_change_contact,
    handle_delete_contact,
    add_email_to_contact,
    handle_show_phone,
    handle_show_email,
    handle_show_all,
    handle_find_contact,
)
from src.handlers.birthday_handlers import (
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays,
)
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
from src.models.address_book import AddressBook
from src.models.notes_book import NotesBook


def main() -> None:
    filename: str = "my_address_book.pkl"
    notes_filename: str = "my_notes.pkl"

    book: AddressBook = load_data(filename, AddressBook)
    notes: NotesBook = load_data(notes_filename, NotesBook)

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
            print("\nAvailable Commands:")
            print(get_help_table())

        elif command == "add":
            print(handle_add_contact(args, book))

        elif command == "change":
            print(handle_change_contact(args, book))

        elif command == "delete":
            print(handle_delete_contact(args, book))

        elif command == "phone":
            print(handle_show_phone(args, book))

        elif command == "all":
            print(handle_show_all(book))

        elif command == "add-email":
            print(add_email_to_contact(args, book))

        elif command == "show-email":
            print(handle_show_email(args, book))

        elif command == "add-birthday":
            print(handle_add_birthday(args, book))

        elif command == "show-birthday":
            print(handle_show_birthday(args, book))

        elif command == "birthdays":
            print(handle_birthdays(args, book))

        elif command == "add-address":
            print(handle_add_address(args, book))
        
        elif command == "show-address":
            print(handle_show_address(args, book))

        elif command == "delete-address":
            print(handle_delete_address(args, book))
        
        elif command == "find":
            print(handle_find_contact(args, book))

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

        elif command == "add-tag":
            print(handle_add_tag(args, notes))

        elif command == "remove-tag":
            print(handle_remove_tag(args, notes))

        elif command == "check-tag":
            print(handle_check_tag(args, notes))

        elif command == "find-notes-by-tag":
            print(handle_find_notes_by_tag(args, notes))
        
        else:
            suggestion = suggest_command(command)
            if suggestion:
                print(f"Invalid command. {suggestion}")
            else:
                print("Invalid command. Type 'hello' to see available commands.")


if __name__ == "__main__":
    main()
