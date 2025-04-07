
import shared  # Import the shared file to access the saved character

def expand_prompt(prompt):
    """Modify the prompt to always include the saved character"""

    # Check if a character is saved
    if shared.saved_character:
        prompt = f"{shared.saved_character}, {prompt}"  # Append saved character to prompt

    return prompt
