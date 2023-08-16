# Bot

Discord bot created to hit Glorious Guardian to get those Mythic Medals and ML Landy. Fueled by my yearning for mythic medals in a mobile gacha game called Epic Seven. Built by a guy with way too much freetime. 

This bot uses the Fribbels GW Tracker and meowyih's gear index for data.
It is able to calculate the rarity of equipments and suggest guild war teams using data sourced by the top 30 guilds.

## Features
- Ideal Gear Scores
- Team Composition Advice

## Bot Commands:
```
!gear [starts an interactive session with the user]
!help [list of commands supported]
!gw [starts attack simulation]
```

## Download Dependencies

Download the requirements.txt and Google Chrome.

`pip install -r requirements.txt`

## Run the bot

1. Fill in the environment variables in a .env file located in the same directory as bot.py. It should contain your Discord Bot Token found under the Discord Developer Portal > Bot > Reset Token area.

2. Update the last line of bot.py with your Discord token: `client.run('token')` or add it in a .env fle.

3. Run the bot with `python bot.py`