from typing import List, Optional
from src.models.fields import Name, Phone, Birthday, Address, Email


class Record:
    """A class representing a contact record in the address book.
    
    This class manages all the information associated with a contact including:
    - Name
    - Phone numbers (multiple)
    - Email address
    - Birthday
    - Address
    """

    def __init__(self, name: str) -> None:
        """Initialize a new contact record.
        
        Args:
            name (str): The name of the contact.
        """
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.birthday: Optional[Birthday] = None
        self.address: Address = None
        
    def add_phone(self, phone: str) -> None:
        """Add a new phone number to the contact.
        
        Args:
            phone (str): The phone number to add.
        """
        self.phones.append(Phone(phone))

    def add_email(self, email: str) -> None:
        """Add or update the email address for the contact.
        
        Args:
            email (str): The email address to set.
        """
        self.email = Email(email)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit an existing phone number.
        
        Args:
            old_phone (str): The phone number to replace.
            new_phone (str): The new phone number.
            
        Raises:
            ValueError: If the old phone number is not found.
        """
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError(f"Phone number {old_phone} not found for editing.")

    def find_phone(self, phone: str) -> Phone:
        """Find a specific phone number in the contact's phone list.
        
        Args:
            phone (str): The phone number to find.
            
        Returns:
            Phone: The found phone number object.
            
        Raises:
            ValueError: If the phone number is not found.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError(f"Phone number {phone} not found.")

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the contact.
        
        Args:
            phone (str): The phone number to remove.
            
        Raises:
            ValueError: If the phone number is not found.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found for removal.")

    def remove_email(self) -> None:
        """Remove the email address from the contact.
        
        Raises:
            ValueError: If no email is set.
        """
        if self.email is None:
            raise ValueError("No email to remove.")
        self.email = None

    def add_birthday(self, birthday: str) -> None:
        """Add or update the birthday for the contact.
        
        Args:
            birthday (str): The birthday in DD.MM.YYYY format.
        """
        self.birthday = Birthday(birthday)

    def show_birthday(self) -> str:
        """Get the formatted birthday string.
        
        Returns:
            str: The birthday in DD.MM.YYYY format.
            
        Raises:
            ValueError: If no birthday is set.
        """
        if not self.birthday:
            raise ValueError("Birthday not set.")
        return self.birthday.value.strftime("%d.%m.%Y")
    
    def delete_birthday(self) -> str:
        """Remove the birthday from the contact.
        
        Returns:
            str: A confirmation message.
            
        Raises:
            ValueError: If no birthday is set.
        """
        if not self.birthday:
            raise ValueError("Birthday not set.")
        self.birthday = None
        return f"The birthday has been removed for {self.name.value}"

    def add_address(self, address: List) -> None:
        """Add or update the address for the contact.
        
        Args:
            address (List): List of address components.
        """
        self.address = Address(address)

    def show_address(self) -> str:
        """Get the formatted address string.
        
        Returns:
            str: The formatted address string.
            
        Raises:
            ValueError: If no address is set.
        """
        if self.address:
            return f"Address: {' '.join(self.address.value)} for {self.name.value}"
        raise ValueError("Address not set.")
    
    def delete_address(self) -> str:
        """Remove the address from the contact.
        
        Returns:
            str: A confirmation message.
            
        Raises:
            ValueError: If no address is set.
        """
        if self.address:
            self.address = None
            return f"The address has been removed for {self.name.value}"
        raise ValueError("Address not set.")

    def show_email(self) -> str:
        """Get the email address of the contact.
        
        Returns:
            str: The email address.
            
        Raises:
            ValueError: If no email is set.
        """
        if not self.email:
            raise ValueError("No email set for the contact.")
        return self.email.value

    """This snippet's good for Cmd: 'all'"""

    def __str__(self) -> str:
        """Get a string representation of the contact.
        
        Returns:
            str: A formatted string containing all contact information.
        """
        birthday_str = f", birthday: {self.show_birthday()}" if self.birthday else ""
        email_str = f", email: {self.show_email()}" if self.email else ""
        return f"Contact name: {self.name.value}, phone(s): {'; '.join(p.value for p in self.phones)}{email_str}{birthday_str}"

    def __setstate__(self, state: dict) -> None:
        """Restore the state of the object from a dictionary.
        
        Args:
            state (dict): The dictionary containing the object's state.
        """
        self.__dict__ = state
        if "address" not in self.__dict__:
            self.__dict__["address"] = None
        if "email" not in self.__dict__:
            self.__dict__["email"] = None
        if "birthday" not in self.__dict__:
            self.__dict__["birthday"] = None
