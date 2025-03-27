from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook


from typing import List


@input_error
def handle_add_address(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Please provide contact name")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found")
    elif record.address:
        raise ValueError(f"Address already exists for {name}")

    address_parts = []
    address_fields = ["Street", "City", "Region", "Post-index"]
    for field in address_fields:
        value = input(f"Enter {field}: ")
        if not value.strip():
            raise ValueError(f"{field} cannot be empty.")
        if field == "Post-index" and not value.isdigit():
            raise ValueError("Post-index must contain only digits.")
        address_parts.append(value)

    record.add_address(address_parts)
    return f"Address: {' '.join(address_parts)} added for {name}"


@input_error
def handle_show_address(args: List[str], book: AddressBook) -> None:
    if not args:
        raise IndexError("Please provide contact name.")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found")
    return record.show_address()


@input_error
def handle_delete_address(args: List[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise ValueError("Please provide contact name")

    name = " ".join(args)
    name = book.normalize_name(name)

    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    return record.delete_address()
