"""
Abilities module handle Abilities Character
"""
import random
import logging
from grammar import sentence
from data.import_data import characters, skills


# Update Character Sheet (Resets on bot restart)


def cost(name, resource="alchemy", value=0):
    """
    Adjust Character Resource Values
    """
    characters[name][resource] += value
    log = sentence(f'{name} changed {resource} by {str(value)}\n')
    return log


def deal_pain(name, damage, damage_type="true"):
    """
    Calculates damage taken based on character resistances to type.
    If the type is not listed, there are no resistances. (i.e holy)
    Damage is calculated as a flat reduction based on resistances.
    """
    if damage_type == "magic":
        damage -= characters[name]["spell_resist"]
    if damage_type == "weapon":
        damage -= characters[name]["armor"]
    log = sentence(f'{name} has taken {damage} {damage_type} damage. \n')
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
    crit = random.randrange(0, 20) == 1  # 5% chance
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
    elif skill["type"] == "misc":
        log = sentence('')
    else:
        return "Error"
    return log


def level_scale(level):
    """
    Inputs character level and outputs level scaling
    Level 0: 1
    Levels 1-10: Adds 0.2 for each level past previous statement
    Levels 11-20: Adds 0.25 for each level past previous statement
    Levels 21-30: Adds 0.3 for each level past previous statement
    Levels 31-40: Adds 0.35 for each level past previous statement
    Levels 41-50: Adds 0.4 for each level past previous statement
    Level 50 is max
    """
    depth = level / 10
    if depth > 4:
        return 1 + (0.2 * 10) + (0.25 * (level - 10)) + (0.3 * (level - 20)) + (0.35 * (level - 30)) + (0.4 * (level - 40))
    elif depth > 3:
        return 1 + (0.2 * 10) + (0.25 * (level - 10)) + (0.3 * (level - 20)) + (0.35 * (level - 30))
    elif depth > 2:
        return 1 + (0.2 * 10) + (0.25 * (level - 10)) + (0.3 * (level - 20))
    elif depth > 1:
        return 1 + (0.2 * 10) + (0.25 * (level - 10))
    else:
        return 1 + (0.2 * level)


def transform(character):
    """
    Transform function for characters. Changes certain character's base stats.
    """
    player = characters[character]
    if character == "shai":
        if not player["is_transformed"]:
            player["spell_resist"] += 10 * level_scale(player["level"]) - 10
            player["weapon_power"] = 65 * level_scale(player["level"])
            player["is_transformed"] = True
            return "Shai'Rei transformed to fox form."
        else:
            player["spell_resist"] = characters["shai_human"]["spell_resist"]
            player["weapon_power"] = characters["shai_human"]["weapon_power"]
            return "Shai'Rei returned to human form."


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
        msg += f'{str(i)}. {sentence(eval(effect))}'

    # If a character can't pay the cost, then return without applying effects.

    # Apply Effects (Do damage, Heal etc..)
    msg += apply(player, skill)

    if logging_enabled:
        logging.info(f"Ability casted ({character}, {ability}): {msg}")

    return msg
