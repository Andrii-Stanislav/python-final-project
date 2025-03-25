from typing import List, Optional
from src.models.fields import Name, Phone, Birthday, Email


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def add_email(self, email: str) -> None:
        self.email = Email(email)

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

    def remove_email(self) -> None:
        self.email = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def show_birthday(self) -> str:
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return "Birthday not set"

    def show_email(self) -> str:
        return self.email.value if self.email else "No email set for the contact"

    def __str__(self) -> str:
        phones_str = (
            "; ".join(str(phone) for phone in self.phones)
            if self.phones
            else "No phone numbers"
        )
        email_str = str(self.email) if self.email else "No email set"
        birthday_str = (
            f"{self.birthday.value.strftime('%d.%m.%Y')}"
            if self.birthday
            else "No birthday set"
        )

        return (
            f"Contact name: {self.name.value}, "
            f"phone(s): {phones_str}, "
            f"email: {email_str}, "
            f"birthday: {birthday_str}"
        )

    def __setstate__(self, state: dict) -> None:
        self.__dict__ = state
        if "address" not in self.__dict__:
            self.__dict__["address"] = None
        if "email" not in self.__dict__:
            self.__dict__["email"] = None
        if "birthday" not in self.__dict__:
            self.__dict__["birthday"] = None
