from tabulate import tabulate
from typing import List, Tuple

# Command categories and their commands
COMMAND_CATEGORIES: Dict[str, List[Tuple[str, str]]] = {
    "Contact Management": [
        ("add <name> <phone>", "Add a new contact with phone number"),
        ("change <name> <old_phone> <new_phone>", "Change contact's phone number"),
        ("delete <name>", "Delete a contact"),
        ("phone <name>", "Show contact's phone number"),
        ("all", "Show all contacts"),
        ("add-email <name> <email>", "Add email to contact"),
        ("show-email <name>", "Show contact's email"),
    ],
    "Birthday Management": [
        ("add-birthday <name> <DD.MM.YYYY>", "Add birthday to contact"),
        ("show-birthday <name>", "Show contact's birthday"),
        ("birthdays <days>", "Show upcoming birthdays within specified days"),
    ],
    "Address Management": [
        ("add-address <name>", "Add address to contact"),
        ("show-address <name>", "Show contact's address"),
        ("delete-address <name>", "Delete contact's address"),
    ],
    "Notes Management": [
        ("add-note <title> <content>", "Add a new note"),
        ("edit-note <title> <new_content>", "Edit an existing note"),
        ("delete-note <title>", "Delete a note"),
        ("find-note <keyword>", "Find notes by keyword"),
        ("show-notes", "Show all notes"),
    ],
    "System Commands": [
        ("hello", "Show this help message"),
        ("close/exit", "Exit the application"),
    ]
}

def get_help_table() -> str:
    """
    Generate a formatted table with all available commands.
    
    Returns:
        str: Formatted table string
    """
    all_commands = []
    
    for category, commands in COMMAND_CATEGORIES.items():
        # Add category header with extra spacing
        all_commands.append([f"\n\n{category}", ""])
        # Add commands
        for cmd, desc in commands:
            all_commands.append([cmd, desc])
    
    return tabulate(
        all_commands,
        headers=["Command", "Description"],
        tablefmt="grid",
        colalign=("left", "left")
    ) 