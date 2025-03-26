from typing import List
from src.utils.decorators import input_error
from src.models.notes_book import NotesBook

@input_error
def handle_add_note(args: List[str], book: "NotesBook") -> str:
    if len(args) < 2:
        raise IndexError("Please provide note title and content.")
    title, content = args[0], ' '.join(args[1:])
    return book.add_note(title, content)

@input_error
def handle_find_note(args: List[str], book: "NotesBook") -> str:
    if not args:
        return "Please provide a search keyword."
    
    keyword = " ".join(args).lower() 
    matching_notes = [
        str(note) for note in book.data.values()
        if keyword in note.title.lower() or keyword in note.content.lower()
    ]
    
    return "\n".join(matching_notes) if matching_notes else "No matching notes found."

@input_error
def handle_edit_note(args: List[str], book: "NotesBook") -> str:
    if len(args) < 2:
        raise IndexError("Please provide note title and new content.")
    title, new_content = args[0], ' '.join(args[1:])
    return book.edit_note(title, new_content)

@input_error
def handle_delete_note(args: List[str], book: "NotesBook") -> str:
    if len(args) != 1:
        raise IndexError("Please provide note title.")
    return book.delete_note(args[0])

@input_error
def handle_show_notes(book: "NotesBook") -> str:
    return book.show_all_notes()