from typing import List, Optional
from src.models.fields import Name, Phone, Birthday, Address

class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.address: Address = None
        
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
    
    def add_address(self, address: List) -> None:
        self.address = Address(address)

    def show_address(self) -> str:
        if self.address:
            return f"Address: {' '.join(self.address.value)} for {self.name.value}"
        raise ValueError("Address not set")
    
    def delete_address(self) -> str:
        if self.address:
            self.address = None
            return f"The address has been removed for {self.name.value}"
        raise ValueError("Address not set")

    def __str__(self) -> str:
        birthday_str = f", birthday: {self.show_birthday()}" if self.birthday else ""
        address_str = f", address: {' '.join(self.address.value)}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}{address_str}" 