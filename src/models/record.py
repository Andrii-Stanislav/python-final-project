from typing import List, Optional
from src.models.fields import Name, Phone, Birthday, Address, Email


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.birthday: Optional[Birthday] = None
        self.address: Address = None
        
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError(f"Phone number {old_phone} not found for editing.")

    def find_phone(self, phone: str) -> Phone:
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError(f"Phone number {phone} not found.")

    def remove_phone(self, phone: str) -> None:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found for removal.")

    def remove_email(self) -> None:
        if self.email is None:
            raise ValueError("No email to remove.")
        self.email = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def show_birthday(self) -> str:
        if not self.birthday:
            raise ValueError("Birthday not set.")
        return self.birthday.value.strftime("%d.%m.%Y")

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

    def show_email(self) -> str:
        if not self.email:
            raise ValueError("No email set for the contact.")
        return self.email.value

    """This snippet's good for Cmd: 'all'"""

    def __str__(self) -> str:
        birthday_str = f", birthday: {self.show_birthday()}" if self.birthday else ""
        email_str = f", email: {self.show_email()}" if self.email else ""
        return f"Contact name: {self.name.value}, phone(s): {'; '.join(p.value for p in self.phones)}{email_str}{birthday_str}"

    """This snippet's on Raise Error in __str__ method - Cmd: 'all' need to be fixed"""
    """def __str__(self) -> str:
        def format_phones():
            if not self.phones:
                raise ValueError("No phone numbers set.")
            return "; ".join(str(phone) for phone in self.phones)

        def format_email():
            if not self.email:
                raise ValueError("No email set for the contact.")
            return str(self.email)

        def format_birthday():
            if not self.birthday:
                raise ValueError("Birthday not set.")
            return self.birthday.value.strftime("%d.%m.%Y")

        phones_str = format_phones()
        email_str = format_email()
        birthday_str = format_birthday()

        return (
            f"Contact name: {self.name.value}, "
            f"phone(s): {phones_str}, "
            f"email: {email_str}, "
            f"birthday: {birthday_str}"
        )"""

    def __setstate__(self, state: dict) -> None:
        self.__dict__ = state
        if "address" not in self.__dict__:
            self.__dict__["address"] = None
        if "email" not in self.__dict__:
            self.__dict__["email"] = None
        if "birthday" not in self.__dict__:
            self.__dict__["birthday"] = None
