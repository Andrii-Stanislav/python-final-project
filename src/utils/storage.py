import pickle
from typing import Type, TypeVar

T = TypeVar('T', bound=object)

def load_data(filename: str, default_item: Type[T]) -> object:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default_item() 

def save_data(book: object, filename: str) -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)

