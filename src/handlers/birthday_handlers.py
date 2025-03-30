from src.models.address_book import AddressBook
from tabulate import tabulate
from colorama import Fore, Style


def handle_add_birthday(args_str: str, book: AddressBook) -> str:
    """Add a birthday to an existing contact.
    
    Args:
        args_str (str): String containing contact name and birthday date.
                         The last element should be the date, all previous elements form the name.
                         Example: "John Smith: 01.01.2000"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if birthday was added successfully.
        
    Raises:
        ValueError: If contact name or birthday date is not provided.
        KeyError: If contact is not found in the address book.
        ValueError: If the provided date format is invalid.
    """
    [name, date] = args_str.split(":") if args_str else []
    
    if not name or not date:
        raise ValueError("Please provide contact name and birthday date.")

    name = book.normalize_name(name)
    record = book.find(name)

    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    try:
        record.add_birthday(date.strip())
    except ValueError:
        raise ValueError(f"Invalid date format: {date.strip()}")

    return "Birthday added."

def handle_show_birthday(args_str: str, book: AddressBook) -> str:
    """Show the birthday of a given contact.
    
    Args:
        args_str (str): String containing the contact name. Example: "John Smith"
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing the contact's birthday information.
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    args = args_str.split() if args_str else []
    
    if not args:
        raise ValueError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")

    if not record.birthday:
        raise ValueError("No birthday set.")

    return record.show_birthday()

def handle_delete_birthday(args_str: str, book: AddressBook) -> str:
    """Delete the birthday of a given contact.
    
    Args:
        args_str (str): String containing the contact name. Example: "John Smith"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message if birthday was deleted successfully.
        
    Raises:
        ValueError: If contact name is not provided.
        KeyError: If contact is not found in the address book.
    """
    args = args_str.split() if args_str else []
    
    if not args:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)

    if not record:
        raise IndexError(f"Contact '{name}' not found.")

    return record.delete_birthday()

def handle_birthdays(args_str: str, book: AddressBook) -> str:
    """Show upcoming birthdays within the specified number of days.
    
    Args:
        args_str (str): String containing the number of days to look ahead.
                         Example: "7"
        book (AddressBook): The address book instance to search in.
    
    Returns:
        str: Formatted string containing all upcoming birthdays within the specified period.
             Each line contains contact name, birthday date, and celebration date.
        
    Raises:
        ValueError: If number of days is not provided.
        ValueError: If no birthdays are found within the specified period.
    """
    args = args_str.split() if args_str else []
    
    if not args:
        raise ValueError("Please provide number of days.")
        
    date_interval, *_ = args
    upcoming = book.get_upcoming_birthdays(date_interval)
    if len(upcoming) == 0:
        raise ValueError(f"There are no birthdays in the next {date_interval} days.")
    headers = {
        "name": "Name",
        "birthday": "Birthday",
        "congratulation_date": "Congratulation day",
    }
    rowIDs = range(1, int(len(upcoming) + 1))
    return tabulate(
        upcoming, headers=headers, tablefmt="rounded_grid", showindex=rowIDs
    )
