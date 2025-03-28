from typing import List
from src.models.notes_book import NotesBook


def handle_add_note(args: List[str], book: "NotesBook") -> str:
    """Add a new note to the notes book.
    
    Args:
        args (List[str]): List containing note title and content.
                         The first element is the title, all remaining elements form the content.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if note was added successfully.
        
    Raises:
        ValueError: If no note title or content is provided.
    """
    if not args:
        raise ValueError("Please provide note title and content.")
    if len(args) < 2:
        raise ValueError("Please provide both note title and content.")
        
    title, content = args[0], ' '.join(args[1:])
    return book.add_note(title, content)

def handle_find_note(args: List[str], book: "NotesBook") -> str:
    """Search for notes containing the given keyword.
    
    Args:
        args (List[str]): List containing the search keyword(s).
        book (NotesBook): The notes book instance to search in.
    
    Returns:
        str: Formatted string containing all matching notes or "No matching notes found."
             Search is case-insensitive and looks for matches in both title and content.
        
    Raises:
        ValueError: If no search keyword is provided.
    """
    if not args:
        raise ValueError("Please provide a search keyword.")
    
    keyword = " ".join(args).lower() 
    matching_notes = [
        str(note) for note in book.data.values()
        if keyword in note.title.lower() or keyword in note.content.lower()
    ]
    
    return "\n".join(matching_notes) if matching_notes else "No matching notes found."

def handle_edit_note(args: List[str], book: "NotesBook") -> str:
    """Edit an existing note's content.
    
    Args:
        args (List[str]): List containing note title and new content.
                         The first element is the title, all remaining elements form the new content.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if note was edited successfully.
        
    Raises:
        ValueError: If no note title or new content is provided.
    """
    if not args:
        raise ValueError("Please provide note title and new content.")
    if len(args) < 2:
        raise ValueError("Please provide both note title and new content.")
        
    title, new_content = args[0], ' '.join(args[1:])
    return book.edit_note(title, new_content)

def handle_delete_note(args: List[str], book: "NotesBook") -> str:
    """Delete a note by its title.
    
    Args:
        args (List[str]): List containing the note title.
        book (NotesBook): The notes book instance to modify.
    
    Returns:
        str: Success message if note was deleted successfully.
        
    Raises:
        ValueError: If no note title is provided.
    """
    if not args:
        raise ValueError("Please provide note title.")
        
    return book.delete_note(args[0])

def handle_show_notes(book: "NotesBook") -> str:
    """Display all notes in the notes book.
    
    Args:
        book (NotesBook): The notes book instance to display.
    
    Returns:
        str: Formatted string containing all notes' information.
    """
    return book.show_all_notes()