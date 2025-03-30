from enum import Enum

class ContactCommands(str, Enum):
    ADD_CONTACT = "Add Contact"
    SHOW_ALL_CONTACTS = "Show All Contacts"
    FIND_CONTACT = "Find Contact"
    DELETE_CONTACT = "Delete Contact"
    ADD_EMAIL = "Add Email"
    CHANGE_PHONE = "Change Phone"
    SHOW_EMAIL = "Show Email"
    SEARCH_CONTACT = "Search Contact"

class AddressCommands(str, Enum):
    ADD_ADDRESS = "Add Address"
    SHOW_ADDRESS = "Show Address"
    DELETE_ADDRESS = "Delete Address"

class NoteCommands(str, Enum):
    ADD_NOTE = "Add Note"
    SHOW_ALL_NOTES = "Show All Notes"
    FIND_NOTE = "Find Note"
    EDIT_NOTE = "Edit Note"
    DELETE_NOTE = "Delete Note"
    ADD_TAG = "Add Tag"
    REMOVE_TAG = "Remove Tag"
    CHECK_TAG = "Check Tag"
    FIND_NOTES_BY_TAG = "Find Notes by Tag"

class BirthdayCommands(str, Enum):
    ADD_BIRTHDAY = "Add Birthday"
    SHOW_BIRTHDAY = "Show Birthday"
    SHOW_UPCOMING_BIRTHDAYS = "Show Upcoming Birthdays"
    DELETE_BIRTHDAY = "Delete Birthday"

# Dictionary mapping commands to their help messages
COMMAND_HELP_MESSAGES = {
    ContactCommands.ADD_CONTACT: "Enter contact name and phone number. Example: John Smith 1234567890",
    ContactCommands.SHOW_ALL_CONTACTS: "Press Enter to continue...",
    ContactCommands.FIND_CONTACT: "Enter search keyword. Example: John Smith",
    ContactCommands.DELETE_CONTACT: "Enter contact name to delete. Example: John Smith",
    ContactCommands.ADD_EMAIL: "Enter contact name and email. Example: John Smith john@example.com",
    ContactCommands.CHANGE_PHONE: "Enter contact name, old phone, and new phone. Example: John Smith 1234567890 0987654321",
    ContactCommands.SHOW_EMAIL: "Enter contact name. Example: John Smith",
    ContactCommands.SEARCH_CONTACT: "Enter search keyword. Example: John",
    
    AddressCommands.ADD_ADDRESS: "Enter contact name and address. Example: John Smith: 123 Main St, Anytown, USA, 12345",
    AddressCommands.SHOW_ADDRESS: "Enter contact name. Example: John Smith",
    AddressCommands.DELETE_ADDRESS: "Enter contact name. Example: John Smith",
    
    NoteCommands.ADD_NOTE: "Enter note title and content. Example: Meeting Notes Today's meeting was productive",
    NoteCommands.SHOW_ALL_NOTES: "Press Enter to continue...",
    NoteCommands.FIND_NOTE: "Enter search keyword. Example: meeting",
    NoteCommands.EDIT_NOTE: "Enter note title and new content. Example: Meeting Notes Updated meeting notes",
    NoteCommands.DELETE_NOTE: "Enter note title to delete. Example: Meeting Notes",
    NoteCommands.ADD_TAG: "Enter note title and tag. Example: Meeting Notes work",
    NoteCommands.REMOVE_TAG: "Enter note title and tag to remove. Example: Meeting Notes work",
    NoteCommands.CHECK_TAG: "Enter note title and tag to check. Example: Meeting Notes work",
    NoteCommands.FIND_NOTES_BY_TAG: "Enter tag to search. Example: work",
    
    BirthdayCommands.ADD_BIRTHDAY: "Enter contact name and birthday. Example: John Smith: 01.01.2000",
    BirthdayCommands.SHOW_BIRTHDAY: "Enter contact name. Example: John Smith",
    BirthdayCommands.SHOW_UPCOMING_BIRTHDAYS: "Enter number of days to look ahead. Example: 7",
    BirthdayCommands.DELETE_BIRTHDAY: "Enter contact name. Example: John Smith",
} 