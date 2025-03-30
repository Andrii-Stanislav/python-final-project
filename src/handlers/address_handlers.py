from src.models.address_book import AddressBook


def handle_add_address(args_str: str, book: AddressBook) -> str:
    """Add an address to an existing contact.
    
    This function interactively collects address information from the user,
    including street, city, region, and post-index. Each field is validated
    before being added to the contact's record.
    
    Args:
        args_str (str): String containing the contact name and address. Example: "John Smith: 123 Main St, Anytown, USA, 12345"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        str: Success message containing the added address information.
        
    Raises:
        ValueError: If contact name is not provided or contact is not found.
        ValueError: If address already exists for the contact.
    """

    args = args_str.split(":") if args_str else []
    
    if len(args) != 2:
        raise ValueError("Please provide contact name and address.")
    
    name = args[0].strip() if args[0] else ""
    address = args[1].strip() if args[1] else ""
    
    if not name or name.strip() == "":
        raise ValueError("Please provide contact name")


    name = book.normalize_name(name)

    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found")
    elif record.address:
        raise ValueError(f"Address already exists for {name}")

    address_parts = address.split(",") if address else []
    
    if len(address_parts) < 4:
        raise ValueError("Please provide all address fields")

    record.add_address(address_parts)
    return f"Address: {' '.join(address_parts)} added for {name}"

def handle_show_address(args_str: str, book: AddressBook) -> None:
    """Display the address of a given contact.
    
    Args:
        args_str (str): String containing the contact name. Example: "John Smith"
        book (AddressBook): The address book instance to search in.
    
    Returns:
        None: Prints the address information to the console.
        
    Raises:
        ValueError: If contact name is not provided or contact is not found.
    """
    name = args_str.strip()
    
    if not name:
        raise IndexError("Please provide contact name.")

    name = book.normalize_name(name)

    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found")
    return record.show_address()

def handle_delete_address(args_str: str, book: AddressBook) -> None:
    """Delete the address of a given contact.
    
    Args:
        args_str (str): String containing the contact name. Example: "John Smith"
        book (AddressBook): The address book instance to modify.
    
    Returns:
        None: Removes the address from the contact's record.
        
    Raises:
        ValueError: If contact name is not provided or contact is not found.
    """
    name = args_str.strip()
    
    if not name:
        raise ValueError("Please provide contact name")

    name = book.normalize_name(name)

    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    return record.delete_address()
