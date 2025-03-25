import pickle
from src.models.address_book import AddressBook
from src.models.notes_book import NotesBook

def save_data(book: object, filename: str) -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename: str) -> object:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        if "address_book" in filename:
            return AddressBook()  
        elif "notes" in filename:
            return NotesBook()  
        else:
            raise ValueError("Unknown file type")
