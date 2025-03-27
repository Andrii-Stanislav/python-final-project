from typing import List
from src.utils.decorators import input_error
from src.models.address_book import AddressBook
from src.models.fields import AddressField, PostIndex

@input_error
def handle_add_address(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    name, *_ = args 
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    elif record.address:
        raise ValueError(f"Address already exists for {name}")
    address_parts = []
    address_fields = ["Street", "City", "Region", "Post-index"]
    for field in address_fields:
        value = input(f"Enter {field}: ")
        if field == "Post-index":
            address_field = PostIndex(value)
        else:
            address_field = AddressField(value)
        address_parts.append(address_field)
    record.add_address(address_parts)
    return f"Address: {' '.join(address_parts)} added for {name}"

@input_error
def handle_show_address(args: List[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    name, *_ = args 
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    return record.show_address()

@input_error
def handle_delete_address(args: List[str], book: AddressBook) -> None:
    if len(args) < 1:
        raise ValueError("Please provide contact name")
    name, *_ = args 
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    return record.delete_address()