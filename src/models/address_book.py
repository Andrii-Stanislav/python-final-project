from collections import UserDict
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.models.record import Record
from tabulate import tabulate
from colorama import init, Fore, Style


# Initialize colorama with proper settings
init(convert=True, strip=False)

class AddressBook(UserDict[str, Record]):
    """A class for managing a collection of contact records.
    
    This class extends UserDict to provide a dictionary-like interface for storing
    and managing contact records. It includes functionality for adding, finding,
    deleting contacts, and managing their information.
    """

    def normalize_name(self, name: str) -> str:
        """Normalize names to title case and strip leading/trailing spaces.
        
        Args:
            name (str): The name to normalize.
            
        Returns:
            str: The normalized name in title case.
        """
        return " ".join(part.capitalize() for part in name.strip().split())

    def add_record(self, record: Record) -> None:
        """Add a new contact record to the address book.
        
        Args:
            record (Record): The contact record to add.
        """
        normalized_name = self.normalize_name(record.name.value)
        self.data[normalized_name] = record

    def find(self, name: str) -> Optional[Record]:
        """Find a contact record by name.
        
        Args:
            name (str): The name of the contact to find.
            
        Returns:
            Optional[Record]: The found contact record or None if not found.
        """
        normalized_name = self.normalize_name(name)
        return self.data.get(normalized_name)

    def delete(self, name: str) -> None:
        """Delete a contact record from the address book.
        
        Args:
            name (str): The name of the contact to delete.
            
        Raises:
            KeyError: If the contact is not found.
        """
        normalized_name = self.normalize_name(name)
        if normalized_name in self.data:
            del self.data[normalized_name]
        else:
            raise KeyError(f"Contact '{name}' not found.")

    def get_upcoming_birthdays(self, date_interval: str) -> List[Dict[str, str]]:
        """Get a list of upcoming birthdays within the specified date interval.
        
        Args:
            date_interval (str): Number of days to look ahead for birthdays.
            
        Returns:
            List[Dict[str, str]]: List of dictionaries containing birthday information.
            
        Raises:
            ValueError: If date_interval is not a valid integer.
        """
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
        """Add a new contact or update an existing one.
        
        Args:
            name (str): The name of the contact.
            phone (Optional[str]): Optional phone number to add.
            
        Returns:
            str: A message indicating whether the contact was added or updated.
        """
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            record = Record(name)
            self.add_record(record)
            message = f"{Fore.GREEN}Contact added.{Style.RESET_ALL}"
        else:
            message = f"{Fore.YELLOW}Contact updated.{Style.RESET_ALL}"
        if phone:
            record.add_phone(phone)
        return message

    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        """Change a contact's phone number.
        
        Args:
            name (str): The name of the contact.
            old_phone (str): The phone number to replace.
            new_phone (str): The new phone number.
            
        Returns:
            str: A message indicating the phone number was updated.
            
        Raises:
            KeyError: If the contact is not found.
        """
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        record.edit_phone(old_phone, new_phone)
        return f"{Fore.GREEN}Phone number updated.{Style.RESET_ALL}"

    def add_email_to_contact(self, name: str, email: str) -> str:
        """Add or update a contact's email address.
        
        Args:
            name (str): The name of the contact.
            email (str): The email address to add.
            
        Returns:
            str: A message indicating the email was updated.
            
        Raises:
            KeyError: If the contact is not found.
        """
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError(f"Contact not found.")
        record.add_email(email)
        return f"{Fore.GREEN}Contact updated with email address.{Style.RESET_ALL}"

    def show_phone(self, name: str) -> str:
        """Display a contact's phone numbers.
        
        Args:
            name (str): The name of the contact.
            
        Returns:
            str: A formatted string of the contact's phone numbers.
            
        Raises:
            KeyError: If the contact is not found.
        """
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        return f"{Fore.CYAN}{'; '.join(phone.value for phone in record.phones)}{Style.RESET_ALL}"

    def show_email(self, name: str) -> str:
        """Display a contact's email address.
        
        Args:
            name (str): The name of the contact.
            
        Returns:
            str: The contact's email address or a message if none is set.
            
        Raises:
            KeyError: If the contact is not found.
        """
        normalized_name = self.normalize_name(name)
        record = self.find(normalized_name)
        if record is None:
            raise KeyError("Contact not found.")
        return f"{Fore.MAGENTA}{str(record.email) if record.email else 'No email set'}{Style.RESET_ALL}"

    def show_all(self) -> str:
        """Display all contacts in a formatted table.
        
        Returns:
            str: A formatted table containing all contact information.
        """
        if not self.data:
            return f"{Fore.YELLOW}No contacts available.{Style.RESET_ALL}"
        
        # Create table data with colors
        table_data = []
        for i, record in enumerate(self.data.values(), 1):
            row = [
                f"{Fore.WHITE}{i}{Style.RESET_ALL}",
                f"{Fore.CYAN}{record.name.value}{Style.RESET_ALL}",
                f"{Fore.BLUE}{'; '.join(phone.value for phone in record.phones)}{Style.RESET_ALL}",
                f"{Fore.CYAN}{record.email.value if record.email else f'{Fore.RED}No email{Style.RESET_ALL}'}{Style.RESET_ALL}",
                f"{Fore.BLUE}{record.birthday.value.strftime('%d.%m.%Y') if record.birthday else f'{Fore.RED}No birthday{Style.RESET_ALL}'}{Style.RESET_ALL}",
                f"{Fore.CYAN}{' '.join(record.address.value) if record.address else f'{Fore.RED}No address{Style.RESET_ALL}'}{Style.RESET_ALL}"
            ]
            table_data.append(row)
        
        # Create headers with colors
        headers = [
            f"{Fore.WHITE}#{Style.RESET_ALL}",
            f"{Fore.WHITE}Name{Style.RESET_ALL}",
            f"{Fore.WHITE}Phone Numbers{Style.RESET_ALL}",
            f"{Fore.WHITE}Email{Style.RESET_ALL}",
            f"{Fore.WHITE}Birthday{Style.RESET_ALL}",
            f"{Fore.WHITE}Address{Style.RESET_ALL}"
        ]
        
        # Generate table with simple format
        return tabulate(table_data, headers=headers, tablefmt="simple")
    
    def find_contacts(self, query: str) -> List[Record]:
        """Search for contacts matching the given query.
        
        Args:
            query (str): The search query to match against contact information.
            
        Returns:
            List[Record]: List of matching contact records.
        """
        query = query.strip().lower()
        results = []

        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
                continue

            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break  
            
            if record.email and query in record.email.value.lower(): 
                results.append(record)

            if record.birthday and query in record.birthday.value.strftime('%d.%m.%Y'):
                results.append(record)

        return results

