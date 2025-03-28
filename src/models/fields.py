from datetime import datetime, date
from typing import Any
from email_validator import validate_email, EmailNotValidError

import re


class ValidationException(Exception):
    pass


class Field:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.validate_name(value)

    def validate_name(self, value: str) -> None:
        if not re.match(r"^[A-Za-z\s'-]+$", value):
            raise ValidationException(
                "Name must contain only letters, spaces, hyphens, or apostrophes."
            )


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.validate_phone(value)

    def validate_phone(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValidationException("Phone number must be 10 digits")


class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            self.value: date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValidationException("Invalid date format. Use DD.MM.YYYY")

class Address(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)    
    
class Email(Field):
    def __init__(self, email: str) -> None:
        try:
            valid_email = validate_email(email)
            super().__init__(valid_email.normalized)
        except EmailNotValidError:
            raise ValidationException("Please enter a valid email address")
