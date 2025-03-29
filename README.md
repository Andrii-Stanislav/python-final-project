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

3. Install the package:

```bash
pip install -e .
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
