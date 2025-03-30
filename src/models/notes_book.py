from collections import UserDict
from typing import List, Any
from colorama import Fore, Style

class ValidationException(Exception):
    """Custom exception for field validation errors."""
    pass

class TagDuplicateError(Exception):
    """Custom exception for duplicate tag errors."""
    pass

class TagNotFound(Exception):
    """Custom exception for missing tag errors."""
    pass

class Field:
    """Base class for all field types in the notes book.
    
    This class provides basic functionality for storing and string representation of field values.
    """

    def __init__(self, value: Any) -> None:
        """Initialize a new field with a value.
        
        Args:
            value (Any): The value to store in the field.
        """
        self.value = value

    def __str__(self) -> str:
        """Get string representation of the field value.
        
        Returns:
            str: String representation of the field value.
        """
        return str(self.value)

class NoteTitle(Field):
    """Field class for storing and validating note titles.
    
    Titles must be non-empty and not exceed 100 characters.
    """

    def __init__(self, value: str) -> None:
        """Initialize a new note title field.
        
        Args:
            value (str): The title to validate and store.
            
        Raises:
            ValidationException: If the title is empty or too long.
        """
        clear_value = value.strip()
        self.validate_title(clear_value)
        super().__init__(clear_value)

    def validate_title(self, value: str) -> None:
        """Validate the title format.
        
        Args:
            value (str): The title to validate.
            
        Raises:
            ValidationException: If the title is empty or too long.
        """
        if not value:
            raise ValidationException("Note title cannot be empty")
        if len(value) > 100:
            raise ValidationException("Note title must not exceed 100 characters")


class NoteContent(Field):
    """Field class for storing and validating note content.
    
    Content must be non-empty and not exceed 1000 characters.
    """

    def __init__(self, value: str) -> None:
        """Initialize a new note content field.
        
        Args:
            value (str): The content to validate and store.
            
        Raises:
            ValidationException: If the content is empty or too long.
        """
        clear_value = value.strip()
        self.validate_content(clear_value)
        super().__init__(clear_value)

    def validate_content(self, value: str) -> None:
        """Validate the content format.
        
        Args:
            value (str): The content to validate.
            
        Raises:
            ValidationException: If the content is empty or too long.
        """
        if not value:
            raise ValidationException("Note content cannot be empty")
        if len(value) > 1000:
            raise ValidationException("Note content must not exceed 1000 characters")


class Note:
    """A class representing a note in the notes book.
    
    Each note has a title, content, and optional tags.
    """

    def __init__(self, title: str, content: str) -> None:
        """Initialize a new note.
        
        Args:
            title (str): The title of the note.
            content (str): The content of the note.
        """
        self.title = NoteTitle(title).value
        self.content = NoteContent(content).value
        self.tags = [] 

    def add_tag(self, new_tag: str) -> None:
        """Add a new tag to the note.
        
        Args:
            new_tag (str): The tag to add.
            
        Raises:
            TagDuplicateError: If the tag already exists.
        """
        if new_tag in self.tags:
            raise TagDuplicateError(f"Tag '{new_tag}' already exists in the note.")
        self.tags.append(new_tag)

    def remove_tag(self, tag_to_remove: str) -> None:
        """Remove a tag from the note.
        
        Args:
            tag_to_remove (str): The tag to remove.
            
        Raises:
            TagNotFound: If the tag doesn't exist.
        """
        if tag_to_remove not in self.tags:
            raise TagNotFound(f"Tag '{tag_to_remove}' not found in the note.")
        self.tags.remove(tag_to_remove)

    def is_tag_exists(self, tag: str) -> bool:
        """Check if a tag exists in the note.
        
        Args:
            tag (str): The tag to check for.
            
        Returns:
            bool: True if the tag exists, False otherwise.
        """
        return tag in self.tags

    def __str__(self) -> str:
        """Get a string representation of the note.
        
        Returns:
            str: A formatted string containing the note's title, content, and tags.
        """
        return f"{self.title}: {self.content} | Tags: {', '.join(self.tags) if self.tags else 'No tags'}"

class NotesBook(UserDict):
    """A class for managing a collection of notes.
    
    This class extends UserDict to provide a dictionary-like interface for storing
    and managing notes. It includes functionality for adding, finding, editing,
    and deleting notes, as well as managing their tags.
    """

    def __init__(self) -> None:
        """Initialize a new notes book."""
        super().__init__()
        self.data: dict[str, Note] = {}

    def add_note(self, title: str, content: str) -> str:
        """Add a new note to the notes book.
        
        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            
        Returns:
            str: A message indicating whether the note was added.
        """
        try:
            note = Note(title, content)
            self.data[note.title] = note
            return "Note added."
        except ValidationException as e:
            return str(e)

    def find_notes(self, keyword: str) -> List[Note]:
        """Search for notes containing the given keyword in their title.
        
        Args:
            keyword (str): The keyword to search for.
            
        Returns:
            List[Note]: List of matching notes.
        """
        keyword = keyword.strip().lower()
        return [note for title, note in self.data.items() if keyword in title.lower()]

    def edit_note(self, title: str, new_content: str) -> str:
        """Edit the content of an existing note.
        
        Args:
            title (str): The title of the note to edit.
            new_content (str): The new content for the note.
            
        Returns:
            str: A message indicating whether the note was updated.
        """
        if title in self.data:
            self.data[title].content = NoteContent(new_content).value
            return "Note updated."
            
        raise KeyError(f"{Fore.RED}Note not found.{Style.RESET_ALL}")

    def delete_note(self, title: str) -> str:
        """Delete a note from the notes book.
        
        Args:
            title (str): The title of the note to delete.
            
        Returns:
            str: A message indicating whether the note was deleted.
        """
        if title in self.data:
            del self.data[title]
            return "Note deleted."
        
        raise KeyError(f"{Fore.RED}Note not found.{Style.RESET_ALL}")

    def show_all_notes(self) -> str:
        """Display all notes in the notes book.
        
        Returns:
            str: A formatted string containing all notes.
        """
        return "\n".join(str(note) for note in self.data.values()) or "No notes available."

    def add_tag_to_note(self, title: str, new_tag: str) -> str:
        """Add a tag to an existing note.
        
        Args:
            title (str): The title of the note.
            new_tag (str): The tag to add.
            
        Returns:
            str: A message indicating whether the tag was added.
        """
        if title not in self.data:
            raise KeyError(f"{Fore.RED}Note not found.{Style.RESET_ALL}")
        try:
            self.data[title].add_tag(new_tag)
            return f"Tag '{new_tag}' added to note '{title}'."
        except TagDuplicateError as e:
            raise KeyError(f"{Fore.RED}Tag already exists.{Style.RESET_ALL}")

    def remove_tag_from_note(self, title: str, tag_to_remove: str) -> str:
        """Remove a tag from an existing note.
        
        Args:
            title (str): The title of the note.
            tag_to_remove (str): The tag to remove.
            
        Returns:
            str: A message indicating whether the tag was removed.
        """
        if title not in self.data:
            raise KeyError(f"{Fore.RED}Note not found.{Style.RESET_ALL}")
        try:
            self.data[title].remove_tag(tag_to_remove)
            return f"Tag '{tag_to_remove}' removed from note '{title}'."
        except TagNotFound as e:
            raise KeyError(f"{Fore.RED}Tag not found.{Style.RESET_ALL}")

    def is_tag_exists_in_note(self, title: str, tag: str) -> bool:
        """Check if a tag exists in a specific note.
        
        Args:
            title (str): The title of the note.
            tag (str): The tag to check for.
            
        Returns:
            bool: True if the tag exists in the note, False otherwise.
        """
        if title not in self.data:
            return False
        return self.data[title].is_tag_exists(tag)
    
    def find_notes_by_tag(self, tag: str) -> List[Note]:
        """Search for notes containing a specific tag.
        
        Args:
            tag (str): The tag to search for.
            
        Returns:
            List[Note]: List of notes containing the specified tag.
        """
        tag = tag.strip().lower()
        return [note for note in self.data.values() if tag in (t.lower() for t in note.tags)]


