from datetime import datetime, date
from typing import Any
from email_validator import validate_email, EmailNotValidError

import re


class ValidationException(Exception):
    """Custom exception for field validation errors."""
    pass


class Field:
    """Base class for all field types in the address book.
    
    This class provides basic functionality for storing and string representation of field values.
    """

    def __init__(self, value: Any) -> None:
        """Initialize a new field with a value.
        
        Args:
            value (Any): The value to store in the field.
        """
        self.value = value

    def __str__(self) -> str:
        """Get string representation of the field value.
        
        Returns:
            str: String representation of the field value.
        """
        return str(self.value)


class Name(Field):
    """Field class for storing and validating contact names.
    
    Names can only contain letters, spaces, hyphens, and apostrophes.
    """

    def __init__(self, value: str) -> None:
        """Initialize a new name field.
        
        Args:
            value (str): The name to validate and store.
            
        Raises:
            ValidationException: If the name contains invalid characters.
        """
        super().__init__(value)
        self.validate_name(value)

    def validate_name(self, value: str) -> None:
        """Validate the name format.
        
        Args:
            value (str): The name to validate.
            
        Raises:
            ValidationException: If the name contains invalid characters.
        """
        if not re.match(r"^[A-Za-z\s'-]+$", value):
            raise ValidationException(
                "Name must contain only letters, spaces, hyphens, or apostrophes."
            )


class Phone(Field):
    """Field class for storing and validating phone numbers.
    
    Phone numbers must be exactly 10 digits.
    """

    def __init__(self, value: str) -> None:
        """Initialize a new phone field.
        
        Args:
            value (str): The phone number to validate and store.
            
        Raises:
            ValidationException: If the phone number is not 10 digits.
        """
        super().__init__(value)
        self.validate_phone(value)

    def validate_phone(self, value: str) -> None:
        """Validate the phone number format.
        
        Args:
            value (str): The phone number to validate.
            
        Raises:
            ValidationException: If the phone number is not 10 digits.
        """
        if not value.isdigit() or len(value) != 10:
            raise ValidationException("Phone number must be 10 digits")


class Birthday(Field):
    """Field class for storing and validating birthdays.
    
    Birthdays must be in DD.MM.YYYY format.
    """

    def __init__(self, value: str) -> None:
        """Initialize a new birthday field.
        
        Args:
            value (str): The birthday in DD.MM.YYYY format.
            
        Raises:
            ValidationException: If the date format is invalid.
        """
        try:
            self.value: date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValidationException("Invalid date format. Use DD.MM.YYYY")

class Address(Field):
    """Field class for storing contact addresses.
    
    Addresses are stored as a list of components.
    """

    def __init__(self, value: str) -> None:
        """Initialize a new address field.
        
        Args:
            value (str): The address components to store.
        """
        super().__init__(value)    
    
class Email(Field):
    """Field class for storing and validating email addresses.
    
    Uses email-validator package to ensure valid email format.
    """

    def __init__(self, email: str) -> None:
        """Initialize a new email field.
        
        Args:
            email (str): The email address to validate and store.
            
        Raises:
            ValidationException: If the email format is invalid.
        """
        try:
            valid_email = validate_email(email)
            super().__init__(valid_email.normalized)
        except EmailNotValidError:
            raise ValidationException("Please enter a valid email address")
