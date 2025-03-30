from src.models.notes_book import NotesBook
from tabulate import tabulate
from colorama import Fore, Style


def handle_add_note(args_str: str, book: "NotesBook") -> str:
    """Add a new note to the notes book.
    
    Args:
        args_str (str): String containing note title and content.
                         The first element is the title, all remaining elements form the content.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if note was added successfully.
        
    Raises:
        ValueError: If no note title or content is provided.
    """
    args = args_str.split(':') if args_str else []
        
    title = args[0].strip() if args[0] else ""
    content = args[1].strip() if args[1] else ""

    if len(args) != 2 or not title or not content:
        raise ValueError("Please provide note title and content.")
        
    return book.add_note(title, content)

def handle_find_note(args_str: str, book: "NotesBook") -> str:
    """Search for notes containing the given keyword.
    
    Args:
        args_str (str): String containing the search keyword(s).
        book (NotesBook): The notes book instance to search in.
    
    Returns:
        str: Formatted string containing all matching notes or "No matching notes found."
             Search is case-insensitive and looks for matches in both title and content.
        
    Raises:
        ValueError: If no search keyword is provided.
    """
    keyword = args_str.strip().lower()
    
    if not keyword:
        raise ValueError("Please provide a search keyword.")
    
    matching_notes = [
        str(note) for note in book.data.values()
        if keyword in note.title.lower() or keyword in note.content.lower()
    ]
    
    if not matching_notes:
        raise KeyError("No matching notes found.")
    
    return "\n".join(matching_notes)

def handle_edit_note(args_str: str, book: "NotesBook") -> str:
    """Edit an existing note's content.
    
    Args:
        args_str (str): String containing note title and new content.
                         The first element is the title, all remaining elements form the new content.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if note was edited successfully.
        
    Raises:
        ValueError: If no note title or new content is provided.
    """
    args = args_str.split(':') if args_str else []
    
    title = args[0].strip() if args[0] else ""
    content = args[1].strip() if args[1] else ""
    
    if len(args) != 2 or not title or not content:
        raise ValueError("Please provide note title and new content.")
        
    return book.edit_note(title, content)

def handle_delete_note(args_str: str, book: "NotesBook") -> str:
    """Delete a note by its title.
    
    Args:
        args_str (str): String containing the note title.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if note was deleted successfully.
        
    Raises:
        ValueError: If no note title is provided.
    """
    
    if not args_str:
        raise ValueError("Please provide note title.")
        
    return book.delete_note(args_str)

def handle_show_notes(book: "NotesBook") -> str:
    """Display all notes in the notes book.
    
    Args:
        book (NotesBook): The notes book instance to display.
    
    Returns:
        str: Formatted string containing all notes' information in a table format.
    """
    if not book.data:
        return f"{Fore.YELLOW}No notes available.{Style.RESET_ALL}"
    
    # Create table data with colors
    table_data = []
    for i, note in enumerate(book.data.values(), 1):
        row = [
            f"{Fore.WHITE}{i}{Style.RESET_ALL}",
            f"{Fore.CYAN}{note.title}{Style.RESET_ALL}",
            f"{Fore.BLUE}{note.content}{Style.RESET_ALL}",
            f"{Fore.CYAN}{', '.join(note.tags) if note.tags else f'{Fore.RED}No tags{Style.RESET_ALL}'}{Style.RESET_ALL}"
        ]
        table_data.append(row)
    
    # Create headers with colors
    headers = [
        f"{Fore.WHITE}#{Style.RESET_ALL}",
        f"{Fore.WHITE}Title{Style.RESET_ALL}",
        f"{Fore.WHITE}Content{Style.RESET_ALL}",
        f"{Fore.WHITE}Tags{Style.RESET_ALL}"
    ]
    
    return tabulate(table_data, headers=headers, tablefmt="simple")

def handle_add_tag(args_str: str, book: "NotesBook") -> str:
    """Add a tag to a note.
    
    Args:
        args_str (str): String containing note title and tag.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if tag was added successfully.
        
    Raises:
        ValueError: If no note title or tag is provided.
    """
    args = args_str.split(':') if args_str else []
    
    title = args[0].strip() if args[0] else ""
    tag = args[1].strip() if args[1] else ""

    if len(args) != 2 or not title or not tag:
        raise ValueError("Please provide note title and tag.")
        
    return book.add_tag_to_note(title.strip(), tag.strip())

def handle_remove_tag(args_str: str, book: "NotesBook") -> str:
    """Remove a tag from a note.
    
    Args:
        args_str (str): String containing note title and tag to remove.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if tag was removed successfully.
        
    Raises:
        ValueError: If no note title or tag is provided.
    """
    args = args_str.split(':') if args_str else []
    
    title = args[0].strip() if args[0] else ""
    tag_to_remove = args[1].strip() if args[1] else ""

    if len(args) != 2 or not title or not tag_to_remove:
        raise ValueError("Please provide note title and tag to remove.")
        
    return book.remove_tag_from_note(title.strip(), tag_to_remove.strip())

def handle_check_tag(args_str: str, book: "NotesBook") -> str:
    """Check if a tag exists in a note.
    
    Args:
        args_str (str): String containing note title and tag to check.
        book (NotesBook): The notes book instance to search in.
    
    Returns:
        str: Success message if tag exists in note or "Tag does not exist in note."
    """
    args = args_str.split(':') if args_str else []
    
    title = args[0].strip() if args[0] else ""
    tag = args[1].strip() if args[1] else ""
    
    if len(args) != 2 or not title or not tag:
        raise ValueError("Please provide note title and tag to check.")
        
    if book.is_tag_exists_in_note(title.strip(), tag.strip()):
        return f"Tag '{tag}' exists in note '{title}'."
    
    raise KeyError(f"Tag '{tag}' does not exist in note '{title}'.")

def handle_find_notes_by_tag(args_str: str, book: "NotesBook") -> str:
    """Find notes by a specific tag.
    
    Args:
        args_str (str): String containing the tag to search for.
        book (NotesBook): The notes book instance to search in.
    
    Returns:
        str: Formatted string containing all matching notes in a table format.
    """
    tag = args_str.strip()
    
    if not tag:
        raise IndexError("Please provide a tag to search for.")
    
    notes = book.find_notes_by_tag(tag)
    
    if not notes:
        raise KeyError(f"No notes found with tag '{tag}'.")
    
    # Create table data with colors
    table_data = []
    for i, note in enumerate(notes, 1):
        row = [
            f"{Fore.WHITE}{i}{Style.RESET_ALL}",
            f"{Fore.CYAN}{note.title}{Style.RESET_ALL}",
            f"{Fore.BLUE}{note.content}{Style.RESET_ALL}",
            f"{Fore.CYAN}{', '.join(note.tags) if note.tags else f'{Fore.RED}No tags{Style.RESET_ALL}'}{Style.RESET_ALL}"
        ]
        table_data.append(row)
    
    # Create headers with colors
    headers = [
        f"{Fore.WHITE}#{Style.RESET_ALL}",
        f"{Fore.WHITE}Title{Style.RESET_ALL}",
        f"{Fore.WHITE}Content{Style.RESET_ALL}",
        f"{Fore.WHITE}Tags{Style.RESET_ALL}"
    ]
    
    return tabulate(table_data, headers=headers, tablefmt="simple")
