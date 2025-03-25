from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook

@input_error
def handle_add_address(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        return "Please provide contact name"
    name, *_ = args 
    record = book.find(name)
    if record is None:
        return "Contact not found"
    elif record.address:
        return f"Address already exists for {name}"
    address_parts = []
    address_fields = ["Street", "City", "Region", "Post-index"]
    for field in address_fields:
        value = input(f"Enter {field}: ")
        if not value.strip():
            return f"{field} cannot be empty."
        if field == "Post-index" and not value.isdigit():
            return "Post-index must contain only digits."
        address_parts.append(value)
    record.add_address(address_parts)
    return f"Address: {' '.join(address_parts)} added for {name}"