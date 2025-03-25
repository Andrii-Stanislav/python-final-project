import pickle
from typing import Optional
from src.models.address_book import AddressBook

def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 