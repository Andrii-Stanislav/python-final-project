# Contact Management System

A command-line contact management system that allows you to store and manage contacts with their phone numbers and birthdays. The system provides functionality to add, modify, and view contacts, as well as track upcoming birthdays.

## Features

<!-- TODO: edit this list before the end of project development -->

- Add new contacts with phone numbers
- Change existing contact phone numbers
- View all contacts
- View specific contact's phone number
- Add birthday information to contacts
- View contact's birthday
- View upcoming birthdays (within next 7 days)
- Persistent storage of contacts
- Input validation for names and phone numbers
- Birthday notifications with weekend handling

## Requirements

- Python 3.8 or higher
- For external dependencies check `requirements.txt` file

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd python-final-project
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## Project Structure

```
python-final-project/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fields.py      # Field classes (Name, Phone, Birthday)
│   │   ├── record.py      # Record class for contact information
│   │   └── address_book.py # AddressBook class for managing contacts
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── contact_handlers.py  # Contact-related command handlers
│   │   └── birthday_handlers.py # Birthday-related command handlers
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── storage.py     # Data persistence functions
│   │   ├── decorators.py  # Error handling decorators
│   │   └── input_parser.py # Input parsing utilities
│   └── main.py            # Main application entry point
├── README.md
└── run.sh                 # Shell script to run the application
```

## Usage

### Running the Application

You can run the application in two ways:

1. Using the shell script:

```bash
./run.sh
```

2. Directly with Python:

```bash
PYTHONPATH=$PYTHONPATH:. python src/main.py
```

### Available Commands

<!-- TODO: edit this list before the end of project development -->

- `add <name> <phone>` - Add a new contact or update existing one
- `change <name> <old_phone> <new_phone>` - Change contact's phone number
- `phone <name>` - Show contact's phone number
- `all` - Show all contacts
- `add-birthday <name> <DD.MM.YYYY>` - Add birthday to contact
- `show-birthday <name>` - Show contact's birthday
- `birthdays` - Show upcoming birthdays
- `hello` - Get a greeting
- `close` or `exit` - Exit the application

### Examples

<!-- TODO: edit examples before the end of project development -->

```bash
add John 1234567890
add-birthday John 01.01.1990
phone John
birthdays
```

## Data Validation

- Names must contain only letters
- Phone numbers must be 10 digits
- Birthday dates must be in DD.MM.YYYY format

## Data Storage

Contacts are automatically saved to `my_address_book.pkl` when you exit the application. The data is loaded when you start the application.

## Development

The project uses type hints throughout the codebase for better code maintainability and IDE support. You can use tools like `mypy` to check for type errors:

```bash
pip install mypy
mypy src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
