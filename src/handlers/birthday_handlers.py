from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook


@input_error
def handle_add_birthday(args: List[str], book: AddressBook) -> str:
    """Add a birthday to an existing contact."""
    if len(args) < 2:
        raise IndexError("Please provide contact name and birthday date.")

    date = args[-1]
    name = " ".join(args[:-1])

    name = book.normalize_name(name)
    record = book.find(name)

    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    try:
        record.add_birthday(date)
    except ValueError as e:
        return f"Invalid date format: {str(e)}"

    return "Birthday added."


@input_error
def handle_show_birthday(args: List[str], book: AddressBook) -> str:
    """Show the birthday of a given contact."""
    if len(args) != 1:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        raise KeyError(f"Contact '{name}' not found.")

    return record.show_birthday()


@input_error
def handle_birthdays(args: List[str], book: AddressBook) -> str:
    """Show upcoming birthdays in the next 7 days."""
    upcoming = book.get_upcoming_birthdays()

    if len(upcoming) == 0:
        return "There are no birthdays in the next 7 days."

    result = []
    for birthday in upcoming:
        result.append(
            f"{birthday['name']}: birthday on {birthday['birthday']}, celebrate on {birthday['congratulation_date']}"
        )

    return "\n".join(result)
