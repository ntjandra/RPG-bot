# Helper functions to clean up grammar in command outputs without a verbose map.

# Formats a string of text to follow grammar conventions.
def sentence(text):
    # Remove "_" with " " and capitalize first letter
    return text.replace('_', " ").capitalize()
