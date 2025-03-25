from collections import UserDict
from typing import Optional

class Note:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
    
    def __str__(self) -> str:
        return f"{self.title}: {self.content}"

class NotesBook(UserDict[str, Note]):
    def add_note(self, title: str, content: str) -> str:
        self.data[title] = Note(title, content)
        return "Note added."
    
    def find_note(self, title: str) -> Optional[str]:
        note = self.data.get(title)
        return str(note) if note else "Note not found."
    
    def edit_note(self, title: str, new_content: str) -> str:
        note = self.data.get(title)
        if note:
            note.content = new_content
            return "Note updated."
        return "Note not found."
    
    def delete_note(self, title: str) -> str:
        if title in self.data:
            del self.data[title]
            return "Note deleted."
        return "Note not found."
    
    def show_all_notes(self) -> str:
        if not self.data:
            return "No notes available."
        return '\n'.join(str(note) for note in self.data.values())
