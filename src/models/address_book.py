from collections import UserDict
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.models.record import Record


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        del self.data[name]

    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value

            this_year_birthday = birthday.replace(year=today.year)

            # If birthday is in the past, move it to next year
            if this_year_birthday < today:
                this_year_birthday = this_year_birthday.replace(year=today.year + 1)

            # Check if birthday is in the next 7 days
            if 0 <= (this_year_birthday - today).days <= 7:
                congratulation_date = this_year_birthday

                # If birthday is on Saturday or Sunday, move it to Monday
                if congratulation_date.weekday() == 5:  # Saturday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "birthday": congratulation_date.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                    }
                )

        return upcoming_birthdays

    def add_contact(self, name: str, phone: Optional[str] = None) -> str:
        record = self.find(name)
        if record is None:
            record = Record(name)
            self.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        if phone:
            record.add_phone(phone)
        return message

    def add_email_to_contact(self, name: str, email: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError("Contact not found.")
        record.add_email(email)
        return "Contact updated with email address."

    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError("Contact not found.")
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."

    def show_phone(self, name: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError("Contact not found.")
        return "; ".join(phone.value for phone in record.phones)

    def show_email(self, name: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError("Contact not found.")
        return str(record.email) if record.email else "No email set."

    def show_all(self) -> str:
        if not self.data:
            return "No contacts available."
        return "\n".join(str(record) for record in self.data.values())
