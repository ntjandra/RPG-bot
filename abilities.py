from data.import_data import *
# Update Character Sheet (Resets on bot restart)
def cost(name, resource="alchemy", value=0):
    characters[name][resource] += value 
    # TODO: Clean up with better String Concats.
    log =  name + " changed " + resource + " by " + str(value) +' \n'
    return log

# Run through the effects of the skill.
def cast_ability(character, ability):
    skill = skills[character][ability]
    
    msg = ""
    for i, effect in enumerate(skill["effects"]):
        msg += str(i) + ". " + eval(effect)
    return msg

