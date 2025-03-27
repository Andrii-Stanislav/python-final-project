from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook
from tabulate import tabulate


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
    if not args:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")

    if not record.birthday:
        raise ValueError("No birthday set.")

    return record.show_birthday()


@input_error
def handle_delete_birthday(args: List[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        raise KeyError(f"Contact '{name}' not found.")

    return record.delete_birthday()


@input_error
def handle_birthdays(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        return "Please provide number of days"
    date_interval, *_ = args
    upcoming = book.get_upcoming_birthdays(date_interval)
    if len(upcoming) == 0:
        raise ValueError(f"There are no birthdays in the next {date_interval} days.")
    headers = {
        "name": "Name",
        "birthday": "Byrthday",
        "congratulation_date": "Congratulation day",
    }
    rowIDs = range(1, int(len(upcoming) + 1))
    return tabulate(
        upcoming, headers=headers, tablefmt="rounded_grid", showindex=rowIDs
    )
