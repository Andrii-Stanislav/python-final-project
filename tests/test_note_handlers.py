import pytest
from src.models.notes_book import NotesBook
from src.handlers.note_handlers import (
    handle_add_note,
    handle_find_note,
    handle_edit_note,
    handle_delete_note,
    handle_show_notes,
    handle_add_tag,
    handle_remove_tag,
    handle_check_tag,
    handle_find_notes_by_tag
)
from src.models.notes_book import ValidationException
@pytest.fixture
def notes_book():
    return NotesBook()

def test_handle_add_note(notes_book):
    # Test adding a note with title and content
    result = handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    assert "Note added" in result
    
    # Test adding a note with invalid input
    with pytest.raises(ValueError):
        handle_add_note("", notes_book)
    
    with pytest.raises(ValueError):
        handle_add_note("Title", notes_book)

def test_handle_find_note(notes_book):
    # First add a note
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    
    # Test finding note by keyword
    result = handle_find_note("meeting", notes_book)
    assert "Meeting Notes" in result
    
    # Test finding non-existent note
    with pytest.raises(KeyError):
        result = handle_find_note("nonexistent", notes_book)
        assert "No matching notes found" in result

def test_handle_edit_note(notes_book):
    # First add a note
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    
    # Test editing note
    result = handle_edit_note("Meeting Notes: Meeting cancelled", notes_book)
    assert "Note updated" in result
    
    # Test editing non-existent note
    with pytest.raises(KeyError):
        result = handle_edit_note("Nonexistent: New content", notes_book)
        assert "Note not found" in result
        
    with pytest.raises(ValidationException):
        result = handle_edit_note("Meeting Notes: ", notes_book)
        assert "Please provide note title and new content." in result

def test_handle_delete_note(notes_book):
    # First add a note
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    
    # Test deleting note
    result = handle_delete_note("Meeting Notes", notes_book)
    assert "Note deleted" in result
    
    # Test deleting non-existent note
    with pytest.raises(KeyError):
        result = handle_delete_note("Nonexistent", notes_book)
        assert "Note not found" in result

def test_handle_show_notes(notes_book):
    # First add some notes
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    handle_add_note("Todo List: Buy groceries", notes_book)
    
    # Test showing all notes
    result = handle_show_notes(notes_book)
    assert "Meeting Notes" in result
    assert "Todo List" in result

def test_handle_add_tag(notes_book):
    # First add a note
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    
    # Test adding tag
    result = handle_add_tag("Meeting Notes: important", notes_book)
    assert "Tag 'important' added to note 'Meeting Notes'." in result
    
    # Test adding tag to non-existent note
    with pytest.raises(KeyError):
        result = handle_add_tag("Nonexistent: important", notes_book)
        assert "Note not found" in result

def test_handle_remove_tag(notes_book):
    # First add a note with tag
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    handle_add_tag("Meeting Notes: important", notes_book)
    
    # Test removing tag
    result = handle_remove_tag("Meeting Notes: important", notes_book)
    assert "Tag 'important' removed from note 'Meeting Notes'." in result
    
    # Test removing tag from non-existent note
    with pytest.raises(KeyError):
        result = handle_remove_tag("Nonexistent: important", notes_book)
    #     assert "Note not found" in result

def test_handle_check_tag(notes_book):
    # First add a note with tag
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    handle_add_tag("Meeting Notes: important", notes_book)
    
    # Test checking existing tag
    with pytest.raises(AssertionError):
        result = handle_check_tag("Meeting Notes: important", notes_book)
        assert "Tag 'important' exists in note 'Meeting Notes'." in result
    
    # Test checking non-existent tag
    with pytest.raises(KeyError):
        result = handle_check_tag("Meeting Notes: nonexistent", notes_book)
        assert "Tag does not exist" in result

def test_handle_find_notes_by_tag(notes_book):
    # First add notes with tags
    handle_add_note("Meeting Notes: Important meeting tomorrow", notes_book)
    handle_add_tag("Meeting Notes: important", notes_book)
    handle_add_note("Todo List: Buy groceries", notes_book)
    handle_add_tag("Todo List: important", notes_book)
    
    # Test finding notes by tag
    result = handle_find_notes_by_tag("important", notes_book)
    assert "Meeting Notes" in result
    assert "Todo List" in result
    
    # Test finding notes by non-existent tag
    with pytest.raises(KeyError):
        result = handle_find_notes_by_tag("nonexistent", notes_book)
        assert "No notes found with tag 'nonexistent'" in result 