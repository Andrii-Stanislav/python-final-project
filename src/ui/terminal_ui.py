import curses
from typing import List, Callable, Dict

class TerminalUI:
    def __init__(self):
        self.screen = None
        self.current_menu = 0
        self.menus = [
            "Contacts",
            "Notes",
            "Birthdays",
            "Exit"
        ]
        self.contact_actions = [
            "Add Contact",
            "Show All Contacts",
            "Find Contact",
            "Delete Contact",
            "Add Email",
            "Change Phone",
            "Add Address",
            "Back"
        ]
        self.note_actions = [
            "Add Note",
            "Show All Notes",
            "Find Note",
            "Edit Note",
            "Delete Note",
            "Back"
        ]
        self.birthday_actions = [
            "Add Birthday",
            "Show Birthday",
            "Show Upcoming Birthdays",
            "Back"
        ]
        
        # Custom prompts for each command
        self.command_prompts = {
            # Contact prompts
            "Add Contact": "Enter contact data. Example: John Smith 1234567890",
            "Show All Contacts": "Press Enter to continue...",
            "Find Contact": "Enter contact name to search. Example: John Smith",
            "Delete Contact": "Enter contact name to delete. Example: John Smith",
            "Add Email": "Enter contact name and email. Example: John Smith john@example.com",
            "Change Phone": "Enter contact name, old phone, and new phone. Example: John Smith 1234567890 0987654321",
            "Add Address": "Enter contact name. Example: John Smith",
            
            # Note prompts
            "Add Note": "Enter note title and content. Example: Meeting Notes Today's meeting was productive",
            "Show All Notes": "Press Enter to continue...",
            "Find Note": "Enter search keyword. Example: meeting",
            "Edit Note": "Enter note title and new content. Example: Meeting Notes Updated meeting notes",
            "Delete Note": "Enter note title to delete. Example: Meeting Notes",
            
            # Birthday prompts
            "Add Birthday": "Enter contact name and birthday (DD.MM.YYYY). Example: John Smith 01.01.1990",
            "Show Birthday": "Enter contact name. Example: John Smith",
            "Show Upcoming Birthdays": "Enter number of days to look ahead. Example: 7",
        }

    def init_screen(self):
        """Initialize the curses screen."""
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.curs_set(0)
        self.screen.keypad(1)
        curses.noecho()  # Start with echo off

    def draw_menu(self, title: str, options: List[str], selected: int):
        """Draw a menu with the given title and options."""
        self.screen.clear()
        self.screen.addstr(0, 0, title, curses.color_pair(1))
        self.screen.addstr(0, len(title), " " * (curses.COLS - len(title)))
        
        for i, option in enumerate(options):
            if i == selected:
                self.screen.addstr(i + 2, 2, f"> {option}", curses.color_pair(1))
            else:
                self.screen.addstr(i + 2, 2, f"  {option}", curses.color_pair(2))
        
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
        """Show a message to the user."""
        self.screen.clear()
        color = curses.color_pair(3) if is_error else curses.color_pair(2)
        self.screen.addstr(0, 0, message, color)
        self.screen.addstr(curses.LINES - 1, 0, "Press any key to continue...", curses.color_pair(2))
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
                        self.handle_contact_menu(handlers)
                    elif selected_menu == "Notes":
                        self.handle_note_menu(handlers)
                    elif selected_menu == "Birthdays":
                        self.handle_birthday_menu(handlers)
                
        finally:
            self.cleanup()

    def handle_contact_menu(self, handlers: Dict[str, Callable]):
        """Handle the contacts submenu."""
        self.__handle_menu(handlers, self.contact_actions)

    def handle_note_menu(self, handlers: Dict[str, Callable]):
        """Handle the notes submenu."""
        self.__handle_menu(handlers, self.note_actions)

    def handle_birthday_menu(self, handlers: Dict[str, Callable]):
        """Handle the birthdays submenu."""
        self.__handle_menu(handlers, self.birthday_actions)

    def __handle_menu(self, handlers: Dict[str, Callable], menu: List[str]):
        """Handle submenu."""
        selected = 0
        while True:
            self.draw_menu("Birthday Management", menu, selected)
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
                        args = input_str.split() if input_str else []
                        result = handlers[action](args)
                        self.show_message(result)
                    except Exception as e:
                        self.show_message(str(e), is_error=True) 