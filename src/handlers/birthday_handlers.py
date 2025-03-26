from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook

@input_error
def handle_add_birthday(args: List[str], book: AddressBook) -> str:
    if len(args) != 2:
        raise IndexError('Please provide contact name and birthday date.')
    name, date = args
    record = book.find(name)
    if not record:
        raise KeyError('Contact not found.')
    record.add_birthday(date)
    return "Birthday added"

@input_error
def handle_show_birthday(args: List[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise IndexError('Please provide contact name.')
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError('Contact not found.')
    return record.show_birthday()

@input_error
def handle_birthdays(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        return "Please provide number of days"
    date_interval, *_ = args
    upcoming = book.get_upcoming_birthdays(date_interval)
    if len(upcoming) == 0:
        raise ValueError(f"There are no birthdays in the next {date_interval} days.") 
    result = []
    for birthday in upcoming:
        result.append(f"{birthday['name']}: birthday on {birthday['birthday']}, celebrate on {birthday['congratulation_date']}")
    return "\n".join(result)