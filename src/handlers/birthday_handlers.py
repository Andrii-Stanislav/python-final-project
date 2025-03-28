from typing import List
from src.models.address_book import AddressBook


def handle_add_birthday(args: List[str], book: AddressBook) -> str:
    """Add a birthday to an existing contact.
    
    Args:
        args (List[str]): List containing contact name and birthday date.
                         The last element should be the date, all previous elements form the name.
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if birthday was added successfully.
        
    Raises:
        ValueError: If contact name or birthday date is not provided.
        KeyError: If contact is not found in the address book.
        ValueError: If the provided date format is invalid.
    """
    if not args:
        raise ValueError("Please provide contact name and birthday date.")
    if len(args) < 2:
        raise ValueError("Please provide both contact name and birthday date.")

    date = args[-1]
    name = " ".join(args[:-1])

    name = book.normalize_name(name)
    record = book.find(name)

    if not record:
        return f"Contact '{name}' not found."
    try:
        record.add_birthday(date)
    except ValueError as e:
        return f"Invalid date format: {str(e)}"

    return "Birthday added."


def handle_show_birthday(args: List[str], book: AddressBook) -> str:
    """Show the birthday of a given contact.
    
    Args:
        args (List[str]): List containing the contact name.
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's birthday information.
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    if not args:
        raise ValueError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        raise IndexError(f"Contact '{name}' not found.")

    return record.show_birthday()


def handle_birthdays(args: List[str], book: AddressBook) -> str:
    """Show upcoming birthdays within the specified number of days.
    
    Args:
        args (List[str]): List containing the number of days to look ahead.
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing all upcoming birthdays within the specified period.
             Each line contains contact name, birthday date, and celebration date.
        
    Raises:
        ValueError: If number of days is not provided.
        ValueError: If no birthdays are found within the specified period.
    """
    if not args:
        raise ValueError("Please provide number of days.")
        
    date_interval, *_ = args
    upcoming = book.get_upcoming_birthdays(date_interval)
    if len(upcoming) == 0:
        raise ValueError(f"There are no birthdays in the next {date_interval} days.")
        
    result = []
    for birthday in upcoming:
        result.append(f"{birthday['name']}: birthday on {birthday['birthday']}, celebrate on {birthday['congratulation_date']}")
    return "\n".join(result)
