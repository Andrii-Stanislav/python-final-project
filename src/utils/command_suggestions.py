from typing import List, Tuple
from thefuzz import fuzz

# List of all available commands
AVAILABLE_COMMANDS: List[str] = [
    "add",
    "change",
    "delete",
    "phone",
    "all",
    "find",
    "add-email",
    "show-email",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-address",
    "show-address",
    "delete-address",
    "add-note",
    "edit-note",
    "delete-note",
    "find-note",
    "show-notes",
    "hello",
    "close",
    "exit"
]

def find_closest_command(command: str, threshold: int = 60) -> Tuple[str, int]:
    """
    Find the closest matching command using fuzzy string matching.
    
    Args:
        command: The command to match
        threshold: Minimum similarity score (0-100) to consider a match
        
    Returns:
        Tuple of (closest_command, similarity_score)
    """
    best_match = None
    best_score = 0
    
    for available_command in AVAILABLE_COMMANDS:
        score = fuzz.ratio(command.lower(), available_command.lower())
        if score > best_score:
            best_score = score
            best_match = available_command
    
    if best_score >= threshold:
        return best_match, best_score
    return "", 0

def suggest_command(command: str) -> str:
    """
    Suggest a command correction if the input command is invalid.
    
    Args:
        command: The invalid command
        
    Returns:
        Suggestion message or empty string if no good match found
    """
    closest_command, score = find_closest_command(command)
    
    if closest_command:
        return f"Did you mean '{closest_command}'? (similarity: {score}%)"
    return "" 