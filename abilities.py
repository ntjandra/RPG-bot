"""
Abilities module handle Abilities Character
"""
import random
import ast
import logging
from grammar import sentence
from data.import_data import characters , skills


# Update Character Sheet (Resets on bot restart)

# Adjust character resource values
def cost(name, resource="alchemy", value=0):
    """
    Adjust Character Resource Values
    """
    characters[name][resource] += value
    log = sentence(f'{name} changed {resource} by {str(value)}\n')
    return log


def restore(power, scale, multiplier=1):
    """
    Uses Character's Modifiers to restore health. Doesn't crit.
    """
    # Return Character's Healing done.
    total = power * scale * multiplier
    print(power, scale, multiplier)
    return total


def damage(power, scale, multiplier=1):
    """
    Characters Modifiers to calculate damage with Crit Chance
    """
    # Return Character's Damage Dealt.
    total = power * scale * multiplier
    crit = random.randrange(0, 20) == 1 # 5% chance
    print("Crit:", crit)
    print(power, scale, multiplier)
    return (total * 1.5) if crit else total


def apply(character, skill):
    """
    Determines which effects to do based on type.
    """
    if skill["type"] == "magic":
        # Damage with Magic Modifiers
        val = damage(character["spell_power"], skill["scaling"], character["spell_mult"])
        log = sentence(f'Magic damage is {str(val)}\n')
    elif skill["type"] == "weapon":
        # Damage with weapon modifiers
        val = damage(character["weapon_power"], skill["scaling"], character["weapon_mult"])
        log = sentence(f'Weapon damage is {str(val)}\n')
    elif skill["type"] == "support":
        # Create a shield or heal target.
        val = restore(character["spell_power"], skill["scaling"], character["heal_shield_mult"])
        log = sentence(f'Support for {str(val)}\n')
    else:
        return "Error"
    return log


# Run through the effects of the skill.
def cast_ability(character, ability, logging_enabled=False):
    """
    Run through the effects of the skill.
    """
    skill = skills[character][ability]
    player = characters[character]
    msg = ""

    # Initial Resource costs
    for i, effect in enumerate(skill["effects"]):
        msg += f'{str(i)}. {sentence(ast.literal_eval(effect))}'

    # If a character can't pay the cost, then return without applying effects.

    # Apply Effects (Do damage, Heal etc..)
    msg += apply(player, skill)

    if logging_enabled:
        logging.info(f"Ability casted ({character}, {ability}): {msg}")

    return msg
