import json

# Init all relevant files
# Open JSON and returns dictionary
def init_data(file):
    f= open(file)
    data = json.load(f)
    f.close()
    return data

# Init dicts to store rpg sheet data.
characters = init_data('data/characters.json')
skills = init_data('data/skills.json')


