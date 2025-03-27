from collections import UserDict
from typing import List, Any

class ValidationException(Exception):
    pass

class TagDuplicateError(Exception):
    pass

class TagNotFound(Exception):
    pass

class Field:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class NoteTitle(Field):
    def __init__(self, value: str) -> None:
        clear_value = value.strip()
        self.validate_title(clear_value)
        super().__init__(clear_value)

    def validate_title(self, value: str) -> None:
        if not value:
            raise ValidationException("Note title cannot be empty")
        if len(value) > 100:
            raise ValidationException("Note title must not exceed 100 characters")


class NoteContent(Field):
    def __init__(self, value: str) -> None:
        clear_value = value.strip()
        self.validate_content(clear_value)
        super().__init__(clear_value)

    def validate_content(self, value: str) -> None:
        if not value:
            raise ValidationException("Note content cannot be empty")
        if len(value) > 1000:
            raise ValidationException("Note content must not exceed 1000 characters")


class Note:
    def __init__(self, title: str, content: str) -> None:
        self.title = NoteTitle(title).value
        self.content = NoteContent(content).value
        self.tags = [] 

    def add_tag(self, new_tag: str) -> None:
        if new_tag in self.tags:
            raise TagDuplicateError(f"Tag '{new_tag}' already exists in the note.")
        self.tags.append(new_tag)

    def remove_tag(self, tag_to_remove: str) -> None:
        if tag_to_remove not in self.tags:
            raise TagNotFound(f"Tag '{tag_to_remove}' not found in the note.")
        self.tags.remove(tag_to_remove)

    def is_tag_exists(self, tag: str) -> bool:
        return tag in self.tags

    def __str__(self) -> str:
        return f"{self.title}: {self.content} | Tags: {', '.join(self.tags) if self.tags else 'No tags'}"

class NotesBook(UserDict):
    def __init__(self) -> None:
        super().__init__()
        self.data: dict[str, Note] = {}

    def add_note(self, title: str, content: str) -> str:
        try:
            note = Note(title, content)
            self.data[note.title] = note
            return "Note added."
        except ValidationException as e:
            return str(e)

    def find_notes(self, keyword: str) -> List[Note]:
        keyword = keyword.strip().lower()
        return [note for title, note in self.data.items() if keyword in title.lower()]

    def edit_note(self, title: str, new_content: str) -> str:
        if title in self.data:
            try:
                self.data[title].content = NoteContent(new_content).value
                return "Note updated."
            except ValidationException as e:
                return str(e)
        return "Note not found."

    def delete_note(self, title: str) -> str:
        if title in self.data:
            del self.data[title]
            return "Note deleted."
        return "Note not found."

    def show_all_notes(self) -> str:
        return "\n".join(str(note) for note in self.data.values()) or "No notes available."

    def add_tag_to_note(self, title: str, new_tag: str) -> str:
        if title not in self.data:
            return "Note not found."
        try:
            self.data[title].add_tag(new_tag)
            return f"Tag '{new_tag}' added to note '{title}'."
        except TagDuplicateError as e:
            return str(e)

    def remove_tag_from_note(self, title: str, tag_to_remove: str) -> str:
        if title not in self.data:
            return "Note not found."
        try:
            self.data[title].remove_tag(tag_to_remove)
            return f"Tag '{tag_to_remove}' removed from note '{title}'."
        except TagNotFound as e:
            return str(e)

    def is_tag_exists_in_note(self, title: str, tag: str) -> bool:
        if title not in self.data:
            return False
        return self.data[title].is_tag_exists(tag)

