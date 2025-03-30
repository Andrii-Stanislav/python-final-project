# Address Book Manager

A command-line address book application with contact management and note-taking capabilities.

## Features

- Contact Management
  - Add, delete, and search contacts
  - Store phone numbers, emails, and addresses
  - Fuzzy search for contacts
- Note Management
  - Create, edit, and delete notes
  - Tag-based organization
  - Search notes by content or tags
- Birthday Management
  - Track birthdays
  - View upcoming birthdays
  - Birthday notifications

## Requirements

- Python 3.8 or higher
- Terminal with curses support

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/address-book.git
cd address-book
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package and dependencies:

```bash
pip install -e .
pip install -r requirements.txt
```

## Usage

Run the application using one of these methods:

1. Using the installed command:

```bash
address-book
```

2. Using Python module:

```bash
python -m src
```

3. Running the main script directly:

```bash
python src/main.py
```

## Testing

The project includes comprehensive tests for all handlers. To run the tests:

1. Make sure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

2. Run the tests using pytest:

```bash
# Run all tests
pytest

# Run tests with detailed output
pytest -v

# Run tests with print statements visible
pytest -s

# Run tests with coverage report
pytest --cov=src tests/

# Run a specific test file
pytest tests/test_contact_handlers.py

# Run a specific test function
pytest tests/test_contact_handlers.py::test_handle_add_contact
```

The test suite includes:

- Contact handler tests (adding, editing, deleting contacts)
- Note handler tests (adding, editing, deleting notes and tags)
- Birthday handler tests (adding, showing, and managing birthdays)
- Address handler tests (adding, showing, and managing addresses)

## Navigation

- Use arrow keys (↑↓) to navigate menus
- Press Enter to select an option
- Follow on-screen prompts for input
- Press any key to continue after messages

## Data Storage

The application stores data in the following files:

- `my_address_book.pkl`: Contact information
- `my_notes.pkl`: Notes and tags

## Troubleshooting

If you encounter any issues:

1. Make sure your terminal window is large enough
2. Check if your terminal supports curses
3. Verify Python version (3.8 or higher)
4. Ensure all dependencies are installed
5. For test-related issues:
   - Make sure pytest is installed: `pip install pytest pytest-cov`
   - Check if you're in the correct directory
   - Verify that the virtual environment is activated

## License

This project is licensed under the MIT License - see the LICENSE file for details.
