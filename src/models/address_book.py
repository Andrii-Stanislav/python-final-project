from collections import UserDict
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.models.record import Record
import re


class AddressBook(UserDict[str, Record]):
    def normalize_name(self, name: str) -> str:
        """Normalize names to title case and strip leading/trailing spaces"""
        return " ".join(part.capitalize() for part in name.strip().split())

    def add_record(self, record: Record) -> None:
        normalized_name = self.normalize_name(record.name.value)
        self.data[normalized_name] = record

    def find(self, name: str) -> Optional[Record]:
        normalized_name = self.normalize_name(name)
        return self.data.get(normalized_name)

    def delete(self, name: str) -> None:
        normalized_name = self.normalize_name(name)
        if normalized_name in self.data:
            del self.data[normalized_name]
        else:
            raise KeyError(f"Contact '{name}' not found.")

    def get_upcoming_birthdays(self, date_interval: str) -> List[Dict[str, str]]:
        try:
            date_interval = int(date_interval)
        except ValueError:
            raise ValueError("Date interval must be an integer.")
        today = datetime.now().date()
        upcoming_birthdays = {}
        future_date = today + timedelta(days=date_interval)
        for record in self.data.values():
            if not record.birthday:
                continue
            birthday = record.birthday.value
            congratulation_date = birthday.replace(year=today.year)
            if congratulation_date < today:
                congratulation_date = congratulation_date.replace(year=today.year + 1)
            while congratulation_date <= future_date:
                day_of_week = congratulation_date.weekday()
                if day_of_week == 5:
                    congratulation_date += timedelta(days=2)
                elif day_of_week == 6:
                    congratulation_date += timedelta(days=1)
                birthday = datetime(congratulation_date.year, birthday.month, birthday.day,).date()
                year = congratulation_date.year
                if year not in upcoming_birthdays:
                    upcoming_birthdays[year] = []
                upcoming_birthdays[year].append({
                    "name": record.name.value,
                    "birthday": birthday.strftime("%d.%m.%Y"),
                    "congratulation_date": congratulation_date.strftime("%A, %B %d")
                })
                congratulation_date = datetime(congratulation_date.year + 1 , birthday.month, birthday.day,).date()
        sorted_years = sorted(upcoming_birthdays.keys())
        final_result = [entry for year in sorted_years for entry in upcoming_birthdays[year]]
        return final_result

    def add_contact(self, name: str, phone: Optional[str] = None) -> str:
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            record = Record(name)
            self.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        if phone:
            record.add_phone(phone)
        return message

    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."

    def add_email_to_contact(self, name: str, email: str) -> str:
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        record.add_email(email)
        return "Contact updated with email address."

    def show_phone(self, name: str) -> str:
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        return "; ".join(phone.value for phone in record.phones)

    def show_email(self, name: str) -> str:
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        return str(record.email) if record.email else "No email set."

    def show_all(self) -> str:
        if not self.data:
            return "No contacts available."
        return "\n".join(str(record) for record in self.data.values())
