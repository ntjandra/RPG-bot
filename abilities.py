from data.import_data import *
from grammar import sentence
# Update Character Sheet (Resets on bot restart)
def cost(name, resource="alchemy", value=0):
    characters[name][resource] += value 
    # TODO: Clean up with better String Concats.
    log =  sentence(f'{name} changed {resource} by {str(value)}\n')
    return log

# Run through the effects of the skill.
def cast_ability(character, ability):
    skill = skills[character][ability]
    
    msg = ""
    for i, effect in enumerate(skill["effects"]):
        msg += f'{str(i)}. {sentence(eval(effect))}' 
    return msg
