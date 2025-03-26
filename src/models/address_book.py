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

    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError('Contact not found.')
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."

    def show_phone(self, name: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError('Contact not found.')
        return '; '.join(phone.value for phone in record.phones)

    def show_all(self) -> str:
        if not self.data:
            return "No contacts available."
        return '\n'.join(str(record) for record in self.data.values()) 