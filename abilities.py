import random
from data.import_data import *
from grammar import sentence

# Update Character Sheet (Resets on bot restart)

# Adjust character resource values
def cost(name, resource="alchemy", value=0):
    characters[name][resource] += value 
    log =  sentence(f'{name} changed {resource} by {str(value)}\n')
    return log

# Uses Character's Modifiers to restore health. Doesn't crit.
def restore(power, scale, multiplier=1):
    # Return Character's Healing done.
    total = power * scale * multiplier
    print (power, scale, multiplier)
    return total

# Characters Modifiers to calculate damage with Crit Chance
def damage(power, scale, multiplier=1):
    # Return Character's Damage Dealt.
    total = power * scale * multiplier
    crit = True if random.randrange(0, 20) == 1 else False # 5% chance
    print ("Crit:", crit)
    print (power, scale, multiplier)
    return (total * 1.5) if crit else total

# Determines which effects to do based on type.
def apply(character, skill):
    match skill["type"]:
        case "magic":
            # Damage with Magic Modifiers
            val = damage(character["spell_power"], skill["scaling"], character["spell_mult"])
            log = sentence(f'Magic damage is {str(val)}\n')
        case "weapon":
            # Damage with weapon modifiers
            val = damage(character["weapon_power"], skill["scaling"], character["weapon_mult"])
            log = sentence(f'Weapon damage is {str(val)}\n')
        case "support":
            # Create a shield or heal target.
            val = restore(character["spell_power"], skill["scaling"], character["heal_shield_mult"])
            log = sentence(f'Support for {str(val)}\n')
        case None:
            return "Error"
    return log 


# Run through the effects of the skill.
# TODO: Add optional logging.
def cast_ability(character, ability):
    skill = skills[character][ability]
    player = characters[character]
    msg = ""

    # Initial Resource costs
    for i, effect in enumerate(skill["effects"]):
        msg += f'{str(i)}. {sentence(eval(effect))}' 
    
    # If a character can't pay the cost, then return without applying effects.

    # Apply Effects (Do damage, Heal etc..)
    msg += apply(player, skill)

    return msg
