"""
Initalize Data And Handling
"""


import json


def init_data(file):
    """
    Init all relevant files
    Open JSON and returns dictionary
    """
    with open(file,encoding='utf-8') as f:
        data = json.load(f)
    return data

# Init dicts to store rpg sheet data.
characters = init_data('data/characters.json')
skills = init_data('data/skills.json')


def init_party():
    """
    Overwrite previous quicksaves in /data.
    """
    save_file = 'data/characters.json'

    with open (save_file, "w",encoding='utf-8') as outfile:
        json.dump(characters, outfile, indent = 4)

    log = 'All characters have been saved and updated.'
    return log

# Converts existing characters dict into a file as a JSON
def save_player(character, slot=1):
    # Stores existing (local) dict into a temp file
    save_file = f'saves/{character}-{slot}.json'
    with open (save_file, "w",encoding='utf-8') as outfile:
        json.dump(characters[character], outfile, indent = 4)

    log = f'Saved! Load with `!load {character} {slot}.`'
    return log

# Loads a JSON formatted Sheet into /data and reinits it.
def load_player(character, slot=1):
    file = f'saves/{character}-{slot}.json'
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    # Map through the data to fill the characters.json values
    characters[character] = data

    log = f'{character} has been loaded from save slot {slot}.'
    return log