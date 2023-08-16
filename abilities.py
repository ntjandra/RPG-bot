from import_char import *
# Update Character Sheet (Resets on bot restart)
def cost(name, resource="alchemy", value=0):
    character[name][resource] += value 
    return

# Run through the effects of the spells.
def cast_spell(character, ability):
    skill = abilities[character][ability]
    # print(skill)
    # print(skill.keys())
    print(skill["effects"])
    
    for effect in skill["effects"]:
        print(effect)
        eval(effect)
    return


### Index of All Abilities Only works at the end 

abilities = {
    "Maria": {
        "basic": {
            "scaling": 100,
            "damageType": "magic",
            "effects": 
                ["cost(name='Maria', resource='alchemy', value=-25)", "cost(name='Maria', resource='devotion', value=20)"]
        }
    }
}