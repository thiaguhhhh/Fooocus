# shared.py

# Global variable to store the saved character
saved_character = None

def save_character(character):
    """Save a character description globally."""
    global saved_character
    saved_character = character

def get_saved_character():
    """Retrieve the saved character description."""
    return saved_character
