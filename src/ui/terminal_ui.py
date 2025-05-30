import curses
from typing import List, Callable, Dict
from colorama import init as colorama_init
from src.constants.commands import (
    ContactCommands,
    AddressCommands,
    NoteCommands,
    BirthdayCommands,
    COMMAND_HELP_MESSAGES,
)


# Initialize colorama
colorama_init(convert=True, strip=False)

class TerminalUI:
    def __init__(self):
        self.screen = None
        self.current_menu = 0
        self.table_actions = [
            ContactCommands.SHOW_ALL_CONTACTS,
            NoteCommands.SHOW_ALL_NOTES,
            NoteCommands.FIND_NOTES_BY_TAG,
            BirthdayCommands.SHOW_UPCOMING_BIRTHDAYS
        ]
        self.menus = [
            "Contacts",
            "Notes",
            "Birthdays",
            "Exit"
        ]
        self.contact_actions = [
            ContactCommands.ADD_CONTACT,
            ContactCommands.SHOW_ALL_CONTACTS,
            ContactCommands.FIND_CONTACT,
            ContactCommands.DELETE_CONTACT,
            ContactCommands.ADD_EMAIL,
            ContactCommands.CHANGE_PHONE,
            ContactCommands.SHOW_EMAIL,
            ContactCommands.SEARCH_CONTACT,
            AddressCommands.ADD_ADDRESS,
            AddressCommands.SHOW_ADDRESS,
            AddressCommands.DELETE_ADDRESS,
            "Back"
        ]
        self.note_actions = [
            NoteCommands.ADD_NOTE,
            NoteCommands.SHOW_ALL_NOTES,
            NoteCommands.FIND_NOTE,
            NoteCommands.EDIT_NOTE,
            NoteCommands.DELETE_NOTE,
            NoteCommands.ADD_TAG,
            NoteCommands.REMOVE_TAG,
            NoteCommands.CHECK_TAG,
            NoteCommands.FIND_NOTES_BY_TAG,
            "Back"
        ]
        self.birthday_actions = [
            BirthdayCommands.ADD_BIRTHDAY,
            BirthdayCommands.SHOW_BIRTHDAY,
            BirthdayCommands.SHOW_UPCOMING_BIRTHDAYS,
            BirthdayCommands.DELETE_BIRTHDAY,
            "Back"
        ]
        
        # Use the help messages from constants
        self.command_prompts = COMMAND_HELP_MESSAGES

    def init_screen(self):
        """Initialize the curses screen."""
        self.screen = curses.initscr()
        curses.start_color()
        # Initialize all color pairs
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # White
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Red
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Blue
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan
        curses.curs_set(0)
        self.screen.keypad(1)
        curses.noecho()  # Start with echo off

    def draw_menu(self, title: str, options: List[str], selected: int):
        """Draw a menu with the given title and options."""
        try:
            self.screen.clear()
            # Get terminal dimensions
            max_y, max_x = self.screen.getmaxyx()
            
            # Draw title
            if max_y > 0 and max_x > 0:
                title_display = title[:max_x-1]  # Truncate title if too long
                self.screen.addstr(0, 0, title_display, curses.color_pair(1))
                self.screen.addstr(0, len(title_display), " " * (max_x - len(title_display)))
            
            # Draw options
            for i, option in enumerate(options):
                if i + 2 >= max_y:  # Skip if we're out of screen space
                    break
                # Convert enum to string if it's an enum value
                option_str = str(option.value) if hasattr(option, 'value') else str(option)
                option_display = f"{'>' if i == selected else ' '} {option_str}"[:max_x-1]
                try:
                    self.screen.addstr(i + 2, 2, option_display, 
                                     curses.color_pair(1) if i == selected else curses.color_pair(2))
                except curses.error:
                    continue  # Skip if we can't write to this line
            
            self.screen.refresh()
        except curses.error:
            # If we can't draw the menu, show a simple message
            self.screen.clear()
            self.screen.addstr(0, 0, "Terminal window too small. Please resize and try again.")
            self.screen.refresh()

    def get_user_input(self, prompt: str) -> str:
        """Get user input with a prompt."""
        # Show prompt
        try:
            self.screen.addstr(curses.LINES - 2, 0, prompt, curses.color_pair(2))
            self.screen.refresh()
        except curses.error:
            pass

        # Create input window
        input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        input_win.keypad(1)
        
        # Enable echo for input
        curses.echo()
        
        try:
            # Get input using getstr
            input_str = input_win.getstr(0, 0)
            if input_str is None:
                return ""
            return input_str.decode('utf-8')
        except (curses.error, UnicodeDecodeError):
            return ""
        finally:
            # Clean up
            curses.noecho()
            try:
                self.screen.addstr(curses.LINES - 1, 0, " " * curses.COLS)
                self.screen.refresh()
            except curses.error:
                pass

    def show_message(self, message: str, is_error: bool = False):
        """Show a message to the user with support for ANSI color codes."""
        self.screen.clear()
        
        # Split message into lines
        lines = message.split('\n')
        current_y = 0
        
        for line in lines:
            if current_y >= curses.LINES - 1:
                break
                
            # Process ANSI color codes
            current_x = 0
            i = 0
            # Initialize default color
            color = curses.color_pair(3) if is_error else curses.color_pair(2)
            
            while i < len(line):
                if line[i] == '\x1b':  # ANSI escape sequence
                    # Find the end of the escape sequence
                    end = line.find('m', i)
                    if end != -1:
                        # Extract the color code
                        color_code = line[i:end+1]
                        # Convert colorama codes to curses colors
                        if '31' in color_code:  # Red
                            color = curses.color_pair(3)
                        elif '32' in color_code:  # Green
                            color = curses.color_pair(1)
                        else:  # Default to white
                            color = curses.color_pair(2)
                        i = end + 1
                        continue
                
                # Print the character with current color
                try:
                    self.screen.addstr(current_y, current_x, line[i], color)
                    current_x += 1
                except curses.error:
                    pass
                i += 1
            
            current_y += 1
        
        # Show continue prompt
        try:
            self.screen.addstr(curses.LINES - 1, 0, "Press any key to continue...", curses.color_pair(2))
        except curses.error:
            pass
        
        self.screen.refresh()
        self.screen.getch()

    def show_table(self, table_str: str):
        """Show a table with support for ANSI color codes."""
        self.screen.clear()
        
        # Split table into lines
        lines = table_str.split('\n')
        current_y = 0
        
        for line in lines:
            if current_y >= curses.LINES - 1:
                break
                
            # Process ANSI color codes
            current_x = 0
            i = 0
            # Initialize default color
            color = curses.color_pair(2)  # Default to white
            
            while i < len(line):
                if line[i] == '\x1b':  # ANSI escape sequence
                    # Find the end of the escape sequence
                    end = line.find('m', i)
                    if end != -1:
                        # Extract the color code
                        color_code = line[i:end+1]
                        # Convert colorama codes to curses colors
                        if '31' in color_code:  # Red
                            color = curses.color_pair(3)
                        elif '32' in color_code:  # Green
                            color = curses.color_pair(1)
                        elif '33' in color_code:  # Yellow
                            color = curses.color_pair(4)
                        elif '34' in color_code:  # Blue
                            color = curses.color_pair(5)
                        elif '35' in color_code:  # Magenta
                            color = curses.color_pair(6)
                        elif '36' in color_code:  # Cyan
                            color = curses.color_pair(7)
                        else:  # Default to white
                            color = curses.color_pair(2)
                        i = end + 1
                        continue
                
                # Print the character with current color
                try:
                    self.screen.addstr(current_y, current_x, line[i], color)
                    current_x += 1
                except curses.error:
                    pass
                i += 1
            
            current_y += 1
        
        # Show continue prompt
        try:
            self.screen.addstr(curses.LINES - 1, 0, "Press any key to continue...", curses.color_pair(2))
        except curses.error:
            pass
        
        self.screen.refresh()
        self.screen.getch()

    def cleanup(self):
        """Clean up the curses screen."""
        if self.screen:
            curses.echo()  # Restore echo mode
            curses.curs_set(1)  # Restore cursor
            curses.endwin()

    def run(self, handlers: Dict[str, Callable]):
        """Run the main UI loop."""
        try:
            self.init_screen()
            while True:
                self.draw_menu("Address Book Manager", self.menus, self.current_menu)
                key = self.screen.getch()
                
                if key == curses.KEY_UP and self.current_menu > 0:
                    self.current_menu -= 1
                elif key == curses.KEY_DOWN and self.current_menu < len(self.menus) - 1:
                    self.current_menu += 1
                elif key == ord('\n'):  # Enter key
                    selected_menu = self.menus[self.current_menu]
                    if selected_menu == "Exit":
                        break
                    elif selected_menu == "Contacts":
                        self.handle_contact_menu(handlers, "Contacts")
                    elif selected_menu == "Notes":
                        self.handle_note_menu(handlers, "Notes")
                    elif selected_menu == "Birthdays":
                        self.handle_birthday_menu(handlers, "Birthdays")
                
        finally:
            self.cleanup()

    def handle_contact_menu(self, handlers: Dict[str, Callable], title: str):
        """Handle the contacts submenu."""
        self.__handle_menu(handlers, self.contact_actions, title)

    def handle_note_menu(self, handlers: Dict[str, Callable], title: str):
        """Handle the notes submenu."""
        self.__handle_menu(handlers, self.note_actions, title)

    def handle_birthday_menu(self, handlers: Dict[str, Callable], title: str):
        """Handle the birthdays submenu."""
        self.__handle_menu(handlers, self.birthday_actions, title)

    def __handle_menu(self, handlers: Dict[str, Callable], menu: List[str], title: str):
        """Handle submenu."""
        selected = 0
        while True:
            self.draw_menu(f'{title} Management', menu, selected)
            key = self.screen.getch()
            
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(menu) - 1:
                selected += 1
            elif key == ord('\n'):  # Enter key
                action = menu[selected]
                if action == "Back":
                    break
                elif action in handlers:
                    try:
                        prompt = self.command_prompts.get(action, "Enter arguments:")
                        input_str = self.get_user_input(prompt)
                        result = handlers[action](input_str)
                        if action in self.table_actions:
                            self.show_table(result)
                        else:
                            self.show_message(result)
                    except Exception as e:
                        self.show_message(str(e), is_error=True) 