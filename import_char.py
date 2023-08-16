import json
# Init this dict.
character = {}
# Opening JSON file
f = open('character.json') 
# returns JSON object as
# a dictionary
character = json.load(f)
f.close()