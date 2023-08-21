import json

# Init all relevant files
# Open JSON and returns dictionary
def init_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

# Init dicts to store rpg sheet data.
characters = init_data('data/characters.json')
skills = init_data('data/skills.json')


# Converts existing characters dict into a file as a JSON
def save_player(character, slot=1):
    # Stores existing (local) dict into a temp file
    print("saving")
    save_file = f'saves/{character}-{slot}.json'
    with open (save_file, "w") as outfile:
        json.dump(characters[character], outfile, indent = 4) 

    log = f'Saved! Load with `!load {character} {slot}.`'
    return log

# Loads a JSON formatted Sheet into /data and reinits it.
def load_player(character, slot=1):
    file = f'saves/{character}-{slot}.json'
    f = open(file)
    data = json.load(f)
    f.close()
    
    # Map through the data to fill the characters.json values
    characters[character] = data

    log = f'{character} has been loaded from save slot {slot}.'
    return log