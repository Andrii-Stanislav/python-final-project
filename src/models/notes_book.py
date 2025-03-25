from collections import UserDict
from typing import Optional, Any

class ValidationException(Exception):
    pass

class Field:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class NoteTitle(Field):
    def __init__(self, value: str) -> None:
        self.validate_title(value)
        super().__init__(value)

    def validate_title(self, value: str) -> None:
        if not value.strip():
            raise ValidationException("Note title cannot be empty")
        if len(value) > 100:
            raise ValidationException("Note title must not exceed 100 characters")

class NoteContent(Field):
    def __init__(self, value: str) -> None:
        self.validate_content(value)
        super().__init__(value)

    def validate_content(self, value: str) -> None:
        if not value.strip():
            raise ValidationException("Note content cannot be empty")
        if len(value) > 1000:
            raise ValidationException("Note content must not exceed 1000 characters")

class Note:
    def __init__(self, title: str, content: str) -> None:
        self.title = NoteTitle(title).value
        self.content = NoteContent(content).value

    def __str__(self) -> str:
        return f"{self.title}: {self.content}"

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

    def find_note(self, title: str) -> Optional[Note]:
        return self.data.get(title)

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
