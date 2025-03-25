from typing import List, Optional
from src.models.fields import Name, Phone, Birthday

class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
    
    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def remove_phone(self, phone: str) -> None:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)
        
    def show_birthday(self) -> str:
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return "Birthday not set"

    def __str__(self) -> str:
        birthday_str = f", birthday: {self.show_birthday()}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}" 