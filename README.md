# Bot

Discord bot created for an RPG Campaign built for player-use.

## Features
Basic features to speed up calculations and turns. Meant to interface with the character sheet to allow a streamlined UI through the Discord Bot API.

### Bot Commands:
```
!info <character> : shows the character sheet for a given character.
!cast <character> <ability> : applies the effects of an ability.
!help <command> : opens detailed help on the command and inputs.
```

### Sheets
The bot will use the default values in `/data`, as we progress through the campaign please remember to update your character's values and skills.

Supports:
- characters
- skills

## Contribute 
Feel free to add your character specific functions inside the abilities.py. Please ask first before changing bot.py.

If you make changes, create a new branch titled <character-skill_name>. For instance, the deck of cards with random replacement would be `eden-draw` or `eden-draw_deck` for longer names. Once it's ready, submit a Pull Request and I'll take a look in my downtime. Ping me if it's urgent.

### Example 
In the branch `eden-draw_deck`, `skills.json` would contain a new entry with the effect `draw_deck('Eden')`, and a new function called draw_deck(character) that would use random replacement to return a list back.

### Local (Development)

1. Download the requirements.txt in a Virtual Environment (recommended) using [Python](https://www.python.org/downloads/).

`pip install -r requirements.txt`

2. Fill in the environment variables in a .env file located in the same directory as bot.py. It should contain your Discord Bot Token found under the Discord Developer Portal > Bot > Reset Token area. **Important: If you reset the token, let the group know because it will invalidate our old tokens.**

3. Update the last line of bot.py with your Discord token: `client.run('token')` or add it in a .env fle.

4. Run the bot with `python bot.py`

### Hosted (Production)

I'll update this in the future. Planning to use repl.it to host our Discord bot for the next session in a month or so or when you're free after Pharm school.

## Dev Notes

This bot was intended to interface and speed up calculations during combat. Therefore, combat related abilities are prioritized (non-social checks). Altering values is a private atribute and may only be altered through skills or editing the .json file. In the future, I might add a overide. 

### TODOs
- Import/Export sheets
- More Skills supported
- Clean up code for v0.1